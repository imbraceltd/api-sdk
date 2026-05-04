#!/usr/bin/env node
/**
 * Generates clean .md files from MDX source for AI consumption.
 *
 * Input:  website/src/content/docs/**\/*.mdx
 * Output: website/public/**\/*.md  (same directory structure)
 *
 * Each output file is served as a static asset alongside the HTML page:
 *   /sdk/authentication/     ← HTML for humans
 *   /sdk/authentication.md   ← MD for AI agents
 *
 * Usage:
 *   node scripts/generate-llms-md.mjs
 */

import { readFileSync, writeFileSync, mkdirSync, readdirSync, statSync } from 'fs'
import { join, dirname, relative, extname } from 'path'
import { fileURLToPath } from 'url'

const __dirname = dirname(fileURLToPath(import.meta.url))
const DOCS_DIR  = join(__dirname, '../website/src/content/docs')
const OUT_DIR   = join(__dirname, '../website/public')

// ---------------------------------------------------------------------------
// Frontmatter parser — extract title/description, return rest of content
// ---------------------------------------------------------------------------
function parseFrontmatter(content) {
  const match = content.match(/^---\r?\n([\s\S]*?)\r?\n---\r?\n?/)
  if (!match) return { title: '', description: '', body: content }

  const fm = match[1]
  const body = content.slice(match[0].length)

  const titleMatch       = fm.match(/^title:\s*(.+)$/m)
  const descriptionMatch = fm.match(/^description:\s*(.+)$/m)

  return {
    title:       titleMatch       ? titleMatch[1].trim().replace(/^['"]|['"]$/g, '')       : '',
    description: descriptionMatch ? descriptionMatch[1].trim().replace(/^['"]|['"]$/g, '') : '',
    body,
  }
}

// ---------------------------------------------------------------------------
// Strip MDX/Astro/Starlight-specific syntax from body
// ---------------------------------------------------------------------------
function stripMdx(body) {
  let out = body

  // Protect code blocks from being modified — replace with placeholders
  const codeBlocks = []
  out = out.replace(/```[\s\S]*?```/g, (match) => {
    codeBlocks.push(match)
    return `\x00CODE${codeBlocks.length - 1}\x00`
  })

  // Remove top-level MDX import statements (now safe — code blocks are protected)
  out = out.replace(/^import\s[^\n]+\n?/gm, '')

  // Remove AuthOnly wrapper (keep children)
  out = out.replace(/<AuthOnly[^>]*>/g, '')
  out = out.replace(/<\/AuthOnly>/g, '')

  // Remove Tabs wrapper (keep children)
  out = out.replace(/<Tabs[^/]*?>/g, '')
  out = out.replace(/<\/Tabs>/g, '')

  // Remove TabItem wrapper (keep children)
  out = out.replace(/<TabItem[^>]*>/g, '')
  out = out.replace(/<\/TabItem>/g, '')

  // Remove Steps wrapper (keep children)
  out = out.replace(/<Steps>/g, '')
  out = out.replace(/<\/Steps>/g, '')

  // Remove CardGrid wrapper (keep children)
  out = out.replace(/<CardGrid>/g, '')
  out = out.replace(/<\/CardGrid>/g, '')

  // Convert <Card title="..."> content </Card> → ### title\n\ncontent
  out = out.replace(/<Card\s[^>]*title="([^"]+)"[^>]*>([\s\S]*?)<\/Card>/g, (_, title, inner) => {
    return `### ${title}\n\n${inner.trim()}\n`
  })

  // Convert <LinkCard title="..." description="..." href="..."/> → - [title](href): description
  out = out.replace(/<LinkCard\s[^>]*title="([^"]+)"[^>]*description="([^"]+)"[^>]*href="([^"]+)"[^\/>]*\/>/g,
    (_, title, desc, href) => `- [${title}](${href}): ${desc}`)
  // Fallback: remove any remaining LinkCard
  out = out.replace(/<LinkCard[^/]*\/>/g, '')

  // Convert :::note/tip/caution/danger ... ::: → blockquote
  out = out.replace(/:::(note|tip|caution|danger)\n?([\s\S]*?):::/g, (_, _type, inner) =>
    inner.trim().split('\n').map(l => `> ${l}`).join('\n') + '\n'
  )

  // Convert <Aside ...> ... </Aside> → blockquote
  out = out.replace(/<Aside[^>]*>([\s\S]*?)<\/Aside>/g, (_, inner) =>
    inner.trim().split('\n').map(l => `> ${l}`).join('\n') + '\n'
  )

  // Remove <div ...> and </div>
  out = out.replace(/<div[^>]*>/g, '')
  out = out.replace(/<\/div>/g, '')

  // Remove <span ...> wrapper (keep text)
  out = out.replace(/<span[^>]*>([\s\S]*?)<\/span>/g, '$1')

  // Remove remaining JSX self-closing tags that produce no useful text
  out = out.replace(/<[A-Z][A-Za-z]*[^>]*\/>/g, '')

  // Remove remaining JSX open/close tags for unknown components
  out = out.replace(/<[A-Z][A-Za-z]*[^>]*>/g, '')
  out = out.replace(/<\/[A-Z][A-Za-z]*>/g, '')

  // Collapse 3+ blank lines to 2
  out = out.replace(/\n{3,}/g, '\n\n')

  // Restore code blocks
  out = out.replace(/\x00CODE(\d+)\x00/g, (_, i) => codeBlocks[Number(i)])

  return out.trim()
}

// ---------------------------------------------------------------------------
// Build the final .md content
// ---------------------------------------------------------------------------
function buildMarkdown(srcPath) {
  const raw = readFileSync(srcPath, 'utf8')
  const { title, description, body } = parseFrontmatter(raw)

  const header = [
    title       ? `# ${title}` : '',
    description ? `\n> ${description}` : '',
  ].filter(Boolean).join('\n')

  const cleaned = stripMdx(body)

  return [header, cleaned].filter(Boolean).join('\n\n') + '\n'
}

// ---------------------------------------------------------------------------
// Walk docs directory and generate .md files
// ---------------------------------------------------------------------------
function walk(dir, callback) {
  for (const entry of readdirSync(dir)) {
    const full = join(dir, entry)
    if (statSync(full).isDirectory()) {
      walk(full, callback)
    } else if (extname(entry) === '.mdx') {
      callback(full)
    }
  }
}

const SKIP_LOCALES = ['vi', 'zh-cn', 'zh-tw']

let count = 0

walk(DOCS_DIR, (srcPath) => {
  const rel     = relative(DOCS_DIR, srcPath)        // e.g. sdk/authentication.mdx
  const topDir  = rel.split(/[\\/]/)[0]
  if (SKIP_LOCALES.includes(topDir)) return          // English only

  const outRel  = rel.replace(/\.mdx$/, '.md')       // sdk/authentication.md
  const outPath = join(OUT_DIR, outRel)

  mkdirSync(dirname(outPath), { recursive: true })

  const md = buildMarkdown(srcPath)
  writeFileSync(outPath, md, 'utf8')

  console.log(`  ✓ ${outRel}`)
  count++
})

console.log(`\nGenerated ${count} .md files → website/public/`)
