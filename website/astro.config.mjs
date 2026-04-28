import { defineConfig } from 'astro/config'
import starlight from '@astrojs/starlight'
import { visit } from 'unist-util-visit'

const isProd = process.env.NODE_ENV === 'production'
const base = isProd ? '/api-sdk' : '/'

// Astro does not auto-prefix the configured `base` onto root-relative links
// in markdown content (e.g. `[Auth](/sdk/authentication/)`). Sidebar entries
// and Starlight components handle base prefixing themselves, but markdown
// links would render as `/sdk/authentication/` and 404 in production where
// the site is served from `/api-sdk/`. This plugin prefixes the base onto
// internal anchor hrefs.
function rehypePrefixBase() {
  const trimmedBase = base.replace(/\/$/, '')
  if (!trimmedBase) return () => () => {}
  return () => (tree) => {
    visit(tree, 'element', (node) => {
      if (node.tagName !== 'a' || !node.properties) return
      const href = node.properties.href
      if (typeof href !== 'string') return
      if (!href.startsWith('/') || href.startsWith('//')) return
      if (href.startsWith(trimmedBase + '/') || href === trimmedBase) return
      node.properties.href = trimmedBase + href
    })
  }
}

export default defineConfig({
  site: 'https://imbraceltd.github.io',
  base,
  markdown: {
    rehypePlugins: [rehypePrefixBase()],
  },
  integrations: [
    starlight({
      favicon: '/favicon.svg',
      title: 'Imbrace SDK',
      description: 'Official documentation for the Imbrace TypeScript and Python SDKs.',
      logo: {
        src: './src/assets/imbrace_logo.svg',
        replacesTitle: true
      },
      social: {
        github: 'https://github.com/imbraceltd/api-sdk',
      },
      defaultLocale: 'root',
      locales: {
        root:    { label: 'English',   lang: 'en' },
        vi:      { label: 'Tiếng Việt', lang: 'vi' },
        'zh-cn': { label: '简体中文',   lang: 'zh-CN' },
        'zh-tw': { label: '繁體中文',   lang: 'zh-TW' },
      },
      customCss: [
        './src/styles/custom.css',
      ],
      components: {
        SocialIcons: './src/components/SocialIcons.astro',
      },
      sidebar: [
        {
          label: 'Getting Started',
          translations: { vi: 'Bắt Đầu', 'zh-CN': '快速开始', 'zh-TW': '快速開始' },
          items: [
            {
              label: 'Overview',
              translations: { vi: 'Tổng Quan', 'zh-CN': '概览', 'zh-TW': '概覽' },
              link: '/getting-started/overview/',
            },
            {
              label: 'Setup Guide',
              translations: { vi: 'Hướng Dẫn Cài Đặt', 'zh-CN': '安装指南', 'zh-TW': '安裝指南' },
              link: '/getting-started/setup/',
            },
          ],
        },
        {
          label: 'SDK',
          translations: { vi: 'SDK', 'zh-CN': 'SDK', 'zh-TW': 'SDK' },
          items: [
            { label: 'Overview',         link: '/sdk/overview/' },
            { label: 'Installation',     link: '/sdk/installation/' },
            { label: 'Quick Start',      link: '/sdk/quick-start/' },
            { label: 'Authentication',   link: '/sdk/authentication/' },
            { label: 'Full Flow Guide',  link: '/sdk/full-flow-guide/' },
            { label: 'Resources',        link: '/sdk/resources/' },
            { label: 'AI Agent',         link: '/sdk/ai-agent/' },
            { label: 'Error Handling',   link: '/sdk/error-handling/' },
            { label: 'Integrations',     link: '/sdk/integrations/' },
            { label: 'Local Testing',    link: '/sdk/local-testing/' },
          ],
        },
        {
          label: 'Guides',
          translations: { vi: 'Hướng Dẫn', 'zh-CN': '指南', 'zh-TW': '指南' },
          items: [
            {
              label: 'Testing Guide',
              translations: { vi: 'Hướng Dẫn Test', 'zh-CN': '测试指南', 'zh-TW': '測試指南' },
              link: '/guides/testing/',
            },
            {
              label: 'Troubleshooting',
              translations: { vi: 'Lỗi Thường Gặp', 'zh-CN': '常见问题', 'zh-TW': '常見問題' },
              link: '/guides/troubleshooting/',
            },
          ],
        },
      ],
      lastUpdated: true,
    }),
  ],
})
