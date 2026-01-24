export { onRenderHtml }

import { renderToString } from 'react-dom/server'
import { escapeInject, dangerouslySkipEscape } from 'vike/server'
import createEmotionCache from '../utils/createEmotionCache'
import createEmotionServer from '@emotion/server/create-instance'
import Layout from './_Layout'

async function onRenderHtml(pageContext) {
  const { Page, urlPathname } = pageContext
  
  // Page-specific titles and descriptions
  const pageMeta = {
    '/': {
      title: 'SynelWeb - Weboldal készítés Sopronban | Webdesign',
      description: 'Professzionális weboldal készítés és webdesign szolgáltatások Sopronban. Modern, reszponzív weboldalak gyors telepítési idővel.'
    },
    '/projektek': {
      title: 'Projektek - SynelWeb',
      description: 'Nézd meg befejezett projektjeinket és weboldalainkat. Portfólió és referenciamunkák.'
    },
    '/szolgaltatasok': {
      title: 'Szolgáltatások és Csomagok - SynelWeb',
      description: 'Weboldal készítés, webdesign és hosting csomagok. Válaszd ki a számodra megfelelő szolgáltatást.'
    },
    '/velemenyek': {
      title: 'Vélemények - SynelWeb',
      description: 'Ügyfeleink véleménye és tapasztalatai a szolgáltatásainkról.'
    },
    '/elerhetoseg': {
      title: 'Elérhetőség és Kapcsolat - SynelWeb',
      description: 'Vedd fel velünk a kapcsolatot! Kérdés, ajánlatkérés vagy konzultáció.'
    },
    '/rolam': {
      title: 'Rólam - SynelWeb',
      description: 'Ismerd meg a csapatot és a SynelWeb történetét.'
    }
  }
  
  const meta = pageMeta[urlPathname] || pageMeta['/']
  
  // Structured data (JSON-LD) for SEO
  const getStructuredData = (pathname) => {
    const baseSchema = {
      "@context": "https://schema.org",
      "@type": "LocalBusiness",
      "name": "SynelWeb",
      "description": "Weboldal készítés és webdesign szolgáltatások Sopronban",
      "url": "https://www.synelweb.hu",
      "address": {
        "@type": "PostalAddress",
        "addressLocality": "Sopron",
        "addressCountry": "HU"
      },
      "priceRange": "$$"
    };

    if (pathname === '/') {
      return [
        baseSchema,
        {
          "@context": "https://schema.org",
          "@type": "Organization",
          "name": "SynelWeb",
          "url": "https://www.synelweb.hu",
          "logo": "https://www.synelweb.hu/lightlogo.svg",
          "sameAs": []
        }
      ];
    }

    if (pathname === '/velemenyek') {
      return [baseSchema];
    }

    if (pathname === '/szolgaltatasok') {
      return [
        baseSchema,
        {
          "@context": "https://schema.org",
          "@type": "Service",
          "name": "Weboldal készítés",
          "provider": {
            "@type": "LocalBusiness",
            "name": "SynelWeb"
          },
          "areaServed": "Sopron, HU"
        }
      ];
    }

    return [baseSchema];
  };

  const structuredData = getStructuredData(urlPathname);
  
  // Create emotion cache for SSR
  const cache = createEmotionCache()
  const { extractCriticalToChunks, constructStyleTagsFromChunks } = createEmotionServer(cache)
  
  // Render app with emotion cache
  const html = renderToString(
    <Layout emotionCache={cache}>
      <Page />
    </Layout>
  )
  
  // Extract critical CSS from emotion
  const emotionChunks = extractCriticalToChunks(html)
  const emotionCss = constructStyleTagsFromChunks(emotionChunks)
  
  return escapeInject`<!DOCTYPE html>
    <html lang="hu">
      <head>
        <meta charset="UTF-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <title>${meta.title}</title>
        <meta name="description" content="${meta.description}" />
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
        <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700&display=swap" rel="stylesheet" />
        <link rel="preconnect" href="https://res.cloudinary.com" />
        ${structuredData.map(schema => 
          dangerouslySkipEscape(`<script type="application/ld+json">${JSON.stringify(schema)}</script>`)
        ).join('')}
        ${dangerouslySkipEscape(emotionCss)}
      </head>
      <body>
        <div id="root">${dangerouslySkipEscape(html)}</div>
      </body>
    </html>`
}
