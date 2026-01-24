export { onRenderClient }

import { hydrateRoot } from 'react-dom/client'
import createEmotionCache from '../utils/createEmotionCache'
import Layout from './_Layout'

async function onRenderClient(pageContext) {
  const { Page } = pageContext
  
  // Scroll to top on navigation
  if (typeof window !== 'undefined') {
    window.scrollTo(0, 0)
  }
  
  // Create emotion cache for client
  const emotionCache = createEmotionCache()
  
  hydrateRoot(
    document.getElementById('root'),
    <Layout emotionCache={emotionCache}>
      <Page />
    </Layout>
  )
}
