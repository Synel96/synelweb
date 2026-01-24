export { onRenderClient }

import { hydrateRoot } from 'react-dom/client'
import { useEffect } from 'react'
import { usePageContext } from 'vike-react/usePageContext'
import createEmotionCache from '../utils/createEmotionCache'
import Layout from './_Layout'

// ScrollToTop component
function ScrollToTop() {
  const pageContext = usePageContext()
  
  useEffect(() => {
    window.scrollTo(0, 0)
  }, [pageContext.urlPathname])
  
  return null
}

async function onRenderClient(pageContext) {
  const { Page } = pageContext
  
  // Create emotion cache for client
  const emotionCache = createEmotionCache()
  
  hydrateRoot(
    document.getElementById('root'),
    <Layout emotionCache={emotionCache}>
      <ScrollToTop />
      <Page />
    </Layout>
  )
}
