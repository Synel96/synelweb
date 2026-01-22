export { onRenderHtml }

import { renderToString } from 'react-dom/server'
import { escapeInject, dangerouslySkipEscape } from 'vike/server'
import createEmotionCache from '../utils/createEmotionCache'
import createEmotionServer from '@emotion/server/create-instance'
import Layout from './_Layout'

async function onRenderHtml(pageContext) {
  const { Page } = pageContext
  
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
        <meta name="description" content="SynelWeb - Weboldal készítés és webdesign szolgáltatások" />
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
        <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700&display=swap" rel="stylesheet" />
        <link rel="preconnect" href="https://res.cloudinary.com" />
        ${dangerouslySkipEscape(emotionCss)}
      </head>
      <body>
        <div id="root">${dangerouslySkipEscape(html)}</div>
      </body>
    </html>`
}
