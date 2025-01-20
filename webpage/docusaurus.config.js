// @ts-check
import {themes as prismThemes} from 'prism-react-renderer';

/** @type {import('@docusaurus/types').Config} */
const config = {
  title: 'STM32 Hardware Design with KiCAD',
  tagline: 'A website for PCB Design with KiCad',
  favicon: 'img/favicon.ico',
  url: 'https://CagriCatik.github.io',
  baseUrl: '/STM32-HW-Design-with-KiCAD/',
  organizationName: 'CagriCatik',
  projectName: 'STM32-HW-Design-with-KiCAD',
  deploymentBranch: 'gh-pages',
  onBrokenLinks: 'ignore',
  onBrokenMarkdownLinks: 'ignore',

  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  presets: [
    [
      'classic',
      {
        docs: {
          sidebarPath: './sidebars.js',
          remarkPlugins: [require('remark-math')], // Add remark-math
          rehypePlugins: [require('rehype-katex')], // Add rehype-katex
          editUrl:
            'https://github.com/facebook/docusaurus/tree/main/packages/create-docusaurus/templates/shared/',
        },
        blog: {
          showReadingTime: true,
          feedOptions: {
            type: ['rss', 'atom'],
            xslt: true,
          },
          editUrl:
            'https://github.com/facebook/docusaurus/tree/main/packages/create-docusaurus/templates/shared/',
        },
        theme: {
          customCss: './src/css/custom.css',
        },
      },
    ],
  ],

  themeConfig: {
    image: 'img/docusaurus-social-card.jpg',
    navbar: {
      title: 'PCB Design with KiCad',
      logo: {
        alt: 'My Site Logo',
        src: 'img/logo.png',
      },
      items: [
        {
          type: 'docSidebar',
          sidebarId: 'IntroSidebar',
          position: 'left',
          label: 'Introduction',
        },
        {
          type: 'docSidebar',
          sidebarId: 'SchematicSidebar',
          position: 'left',
          label: 'Schematics',
        },
        {
          type: 'docSidebar',
          sidebarId: 'LavoutSidebar',
          position: 'left',
          label: 'Layout',
        },
        {
          type: 'docSidebar',
          sidebarId: 'RoutingSidebar',
          position: 'left',
          label: 'Routing',
        },
        {
          type: 'docSidebar',
          sidebarId: 'ManuSidebar',
          position: 'left',
          label: 'Manufacturing',
        },
        {
          type: 'docSidebar',
          sidebarId: 'ScriptSidebar',
          position: 'left',
          label: 'Scripts',
        },
        {
          type: 'docSidebar',
          sidebarId: 'GlossarySidebar',
          position: 'left',
          label: 'Glossary',
        },
        {to: '/blog', label: 'Blog', position: 'left'},
        {
          href: 'https://github.com/CagriCatik/STM32-HW-Design-with-KiCAD',
          label: 'GitHub',
          position: 'right',
        },
      ],
    },
    footer: {
      style: 'dark',
      links: [
        {
          title: 'Documentation',
          items: [
            {
              label: 'Knowledge Base',
              to: '/docs/category/introduction',
            },
            {
              label: 'Recipes',
              to: '/docs/category/recipes',
            },
          ],
        },
        {
          title: 'Projects',
          items: [
            {
              label: 'Project 1',
              href: 'https://github.com/CagriCatik/STM32-HW-Design-with-KiCAD',
            },
            {
              label: 'Project 2',
              href: 'https://github.com/CagriCatik/STM32-HW-Design-with-KiCAD',
            },
            {
              label: 'Project 3',
              href: 'https://github.com/CagriCatik/STM32-HW-Design-with-KiCAD',
            },
          ],
        },
        {
          title: 'More',
          items: [
            {
              label: 'Blog',
              to: '/blog',
            },
            {
              label: 'GitHub',
              href: 'https://github.com/CagriCatik/STM32-HW-Design-with-KiCAD',
            },
          ],
        },
      ],
      copyright: `PCB Design with KiCad`,
    },
    prism: {
      theme: prismThemes.github,
      darkTheme: prismThemes.dracula,
    },
  },

  stylesheets: [
    {
      href: 'https://cdn.jsdelivr.net/npm/katex@0.16.4/dist/katex.min.css',
      type: 'text/css',
      integrity: 'sha384-d6UvP8MjG/jrWTLxz4ph1bEXHVNyMYAx4GqeFPYYR5tWLm4XAoVRSaSejzE/sFs9',
      crossorigin: 'anonymous',
    },
  ],
};

export default config;
