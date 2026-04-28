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
        root:    { label: 'English',   lang: 'en' },
        vi:      { label: 'Tiếng Việt', lang: 'vi' },
        'zh-cn': { label: '简体中文',   lang: 'zh-CN' },
        'zh-tw': { label: '繁體中文',   lang: 'zh-TW' },
      },
      customCss: [
        './src/styles/custom.css',
      ],
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
          label: 'TypeScript SDK',
          items: [
            {
              label: 'Overview',
              translations: { vi: 'Giới Thiệu', 'zh-CN': '概览', 'zh-TW': '概覽' },
              link: '/typescript/overview/',
            },
            {
              label: 'Installation',
              translations: { vi: 'Cài Đặt', 'zh-CN': '安装', 'zh-TW': '安裝' },
              link: '/typescript/installation/',
            },
            {
              label: 'Quick Start',
              translations: { vi: 'Bắt Đầu Nhanh', 'zh-CN': '快速入门', 'zh-TW': '快速入門' },
              link: '/typescript/quick-start/',
            },
            {
              label: 'Authentication',
              translations: { vi: 'Xác Thực', 'zh-CN': '身份验证', 'zh-TW': '身份驗證' },
              link: '/typescript/authentication/',
            },
            {
              label: 'Full Flow Guide',
              translations: { vi: 'Hướng Dẫn Flow Chi Tiết', 'zh-CN': '完整流程指南', 'zh-TW': '完整流程指南' },
              link: '/typescript/full-flow-guide/',
            },
            {
              label: 'Resources',
              translations: { vi: 'Tài Nguyên API', 'zh-CN': 'API 资源', 'zh-TW': 'API 資源' },
              link: '/typescript/resources/',
            },
            {
              label: 'AI Agent',
              translations: { vi: 'AI Agent', 'zh-CN': 'AI Agent', 'zh-TW': 'AI Agent' },
              link: '/typescript/ai-agent/',
            },
            {
              label: 'Error Handling',
              translations: { vi: 'Xử Lý Lỗi', 'zh-CN': '错误处理', 'zh-TW': '錯誤處理' },
              link: '/typescript/error-handling/',
            },
            {
              label: 'Integrations',
              translations: { vi: 'Tích Hợp', 'zh-CN': '集成', 'zh-TW': '整合' },
              link: '/typescript/integrations/',
            },
            {
              label: 'Local Testing',
              translations: { vi: 'Test Local', 'zh-CN': '本地测试', 'zh-TW': '本地測試' },
              link: '/typescript/local-testing/',
            },
          ],
        },
        {
          label: 'Python SDK',
          items: [
            {
              label: 'Overview',
              translations: { vi: 'Giới Thiệu', 'zh-CN': '概览', 'zh-TW': '概覽' },
              link: '/python/overview/',
            },
            {
              label: 'Installation',
              translations: { vi: 'Cài Đặt', 'zh-CN': '安装', 'zh-TW': '安裝' },
              link: '/python/installation/',
            },
            {
              label: 'Authentication',
              translations: { vi: 'Xác Thực', 'zh-CN': '身份验证', 'zh-TW': '身份驗證' },
              link: '/python/authentication/',
            },
            {
              label: 'Quick Start',
              translations: { vi: 'Bắt Đầu Nhanh', 'zh-CN': '快速入门', 'zh-TW': '快速入門' },
              link: '/python/quick-start/',
            },
            {
              label: 'Resources',
              translations: { vi: 'Tài Nguyên API', 'zh-CN': 'API 资源', 'zh-TW': 'API 資源' },
              link: '/python/resources/',
            },
            {
              label: 'AI Agent',
              translations: { vi: 'AI Agent', 'zh-CN': 'AI Agent', 'zh-TW': 'AI Agent' },
              link: '/python/ai-agent/',
            },
            {
              label: 'Error Handling',
              translations: { vi: 'Xử Lý Lỗi', 'zh-CN': '错误处理', 'zh-TW': '錯誤處理' },
              link: '/python/error-handling/',
            },
            {
              label: 'Integrations',
              translations: { vi: 'Tích Hợp', 'zh-CN': '集成', 'zh-TW': '整合' },
              link: '/python/integrations/',
            },
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
