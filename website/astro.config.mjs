import { defineConfig } from 'astro/config'
import starlight from '@astrojs/starlight'

const isProd = process.env.NODE_ENV === 'production'

export default defineConfig({
  site: 'https://imbraceltd.github.io',
  base: isProd ? '/api-sdk' : '/',
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
        root: { label: 'English', lang: 'en' },
        vi: { label: 'Tiếng Việt', lang: 'vi' },
      },
      customCss: [
        './src/styles/custom.css',
      ],
      sidebar: [
        {
          label: 'Getting Started',
          translations: { vi: 'Bắt Đầu' },
          items: [
            {
              label: 'Overview',
              translations: { vi: 'Tổng Quan' },
              link: '/getting-started/overview/',
            },
          ],
        },
        {
          label: 'TypeScript SDK',
          items: [
            {
              label: 'Overview',
              translations: { vi: 'Giới Thiệu' },
              link: '/typescript/overview/',
            },
            {
              label: 'Installation',
              translations: { vi: 'Cài Đặt' },
              link: '/typescript/installation/',
            },
            {
              label: 'Authentication',
              translations: { vi: 'Xác Thực' },
              link: '/typescript/authentication/',
            },
            {
              label: 'Quick Start',
              translations: { vi: 'Bắt Đầu Nhanh' },
              link: '/typescript/quick-start/',
            },
            {
              label: 'Resources',
              translations: { vi: 'Tài Nguyên API' },
              link: '/typescript/resources/',
            },
            {
              label: 'Full Flow Guide',
              translations: { vi: 'Hướng Dẫn Luồng Đầy Đủ' },
              link: '/typescript/full-flow-guide/',
            },
            {
              label: 'Error Handling',
              translations: { vi: 'Xử Lý Lỗi' },
              link: '/typescript/error-handling/',
            },
            {
              label: 'Integrations',
              translations: { vi: 'Tích Hợp' },
              link: '/typescript/integrations/',
            },
            {
              label: 'Local Testing',
              translations: { vi: 'Test Local' },
              link: '/typescript/local-testing/',
            },
          ],
        },
        {
          label: 'Python SDK',
          items: [
            {
              label: 'Overview',
              translations: { vi: 'Giới Thiệu' },
              link: '/python/overview/',
            },
            {
              label: 'Installation',
              translations: { vi: 'Cài Đặt' },
              link: '/python/installation/',
            },
            {
              label: 'Authentication',
              translations: { vi: 'Xác Thực' },
              link: '/python/authentication/',
            },
            {
              label: 'Quick Start',
              translations: { vi: 'Bắt Đầu Nhanh' },
              link: '/python/quick-start/',
            },
            {
              label: 'Resources',
              translations: { vi: 'Tài Nguyên API' },
              link: '/python/resources/',
            },
            {
              label: 'Error Handling',
              translations: { vi: 'Xử Lý Lỗi' },
              link: '/python/error-handling/',
            },
            {
              label: 'Integrations',
              translations: { vi: 'Tích Hợp' },
              link: '/python/integrations/',
            },
          ],
        },
        {
          label: 'Guides',
          translations: { vi: 'Hướng Dẫn' },
          items: [
            {
              label: 'Testing Guide',
              translations: { vi: 'Hướng Dẫn Test' },
              link: '/guides/testing/',
            },
            {
              label: 'Troubleshooting',
              translations: { vi: 'Lỗi Thường Gặp' },
              link: '/guides/troubleshooting/',
            },
          ],
        },
      ],
      lastUpdated: true,
    }),
  ],
})
