import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import Layout from './components/layout/Layout'
import Dashboard from './pages/Dashboard'
import ComplaintBot from './pages/ComplaintBot'
import ClusterExplorer from './pages/ClusterExplorer'
import ResearchInsights from './pages/ResearchInsights'
import History from './pages/History'

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<Dashboard />} />
          <Route path="bot" element={<ComplaintBot />} />
          <Route path="clusters" element={<ClusterExplorer />} />
          <Route path="insights" element={<ResearchInsights />} />
          <Route path="history" element={<History />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Route>
      </Routes>
    </BrowserRouter>
  )
}