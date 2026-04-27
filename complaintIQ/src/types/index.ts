// ─── Classification ───────────────────────────────────────────────────────────

export interface SentimentScores {
  negative: number
  neutral: number
  positive: number
}

export interface ClassifyRequest {
  complaint_text: string
  session_id?: string
}

export interface ClassifyResponse {
  complaint_id: string
  cluster_id: 0 | 1 | 2
  cluster_label: string
  cluster_keywords: string[]
  sentiment: 'negative' | 'neutral' | 'positive'
  sentiment_scores: SentimentScores
  product_hint: string
  processing_ms: number
}

// ─── Response Bot ─────────────────────────────────────────────────────────────

export interface RespondRequest {
  complaint_id: string
  customer_name?: string
  account_ref?: string
  agent_name?: string
}

export interface RespondResponse {
  response_id: string
  draft_response: string
  response_tone: string
  suggested_actions: string[]
  cluster_context: string
  confidence: number
  processing_ms: number
}

// ─── Clusters ─────────────────────────────────────────────────────────────────

export interface ClusterSentimentBreakdown {
  negative?: number
  neutral?: number
  positive?: number
}

export interface Cluster {
  id: 0 | 1 | 2
  label: string
  count: number
  pct: number
  top_keywords: string[]
  product_hint: string
  context: string
  sentiment_breakdown: ClusterSentimentBreakdown
}

export interface ClustersResponse {
  clusters: Cluster[]
  total_clusters: number
}

// ─── Analytics ────────────────────────────────────────────────────────────────

export interface ModelMetrics {
  bert_test_accuracy: number
  bert_test_f1_macro: number
  bert_test_f1_negative: number
  bert_test_f1_neutral: number
  bert_test_f1_positive: number
  training_epochs: number
  training_samples: number
  val_samples: number
  test_samples: number
  max_len: number
  batch_size: number
  learning_rate: number
}

export interface DatasetStats {
  total_source_complaints: number
  working_sample_size: number
  avg_word_count: number
  median_word_count: number
  p95_word_count: number
  redaction_rate_pct: number
  product_categories: number
  num_clusters: number
}

export interface LiveAnalytics {
  total_complaints_processed: number
  total_responses_generated: number
  sentiment_distribution: Record<string, number>
  cluster_distribution: Record<number, number>
}

export interface AnalyticsResponse {
  live: LiveAnalytics
  model_metrics: ModelMetrics
  dataset_stats: DatasetStats
}

// ─── Figures ──────────────────────────────────────────────────────────────────

export interface FigureMetadata {
  key: string
  title: string
  subtitle: string
  notebook: string
  note: string
  url: string
}

// ─── History ──────────────────────────────────────────────────────────────────

export interface ComplaintHistoryItem {
  _id: string
  raw_text: string
  cluster_id: 0 | 1 | 2
  cluster_label: string
  sentiment: 'negative' | 'neutral' | 'positive'
  sentiment_confidence: number
  product_hint: string
  word_count: number
  processing_ms: number
  session_id?: string
  created_at: string
}

export interface HistoryResponse {
  complaints: ComplaintHistoryItem[]
  total: number
  limit: number
  skip: number
}

// ─── Chat State ───────────────────────────────────────────────────────────────

export type MessageRole = 'user' | 'bot' | 'system'

export interface ChatMessage {
  id: string
  role: MessageRole
  content: string
  timestamp: Date
  classification?: ClassifyResponse
  response?: RespondResponse
  isLoading?: boolean
}

// ─── API Wrapper ──────────────────────────────────────────────────────────────

export interface APIResponse<T> {
  success: boolean
  data: T
  message?: string
  error?: string
}