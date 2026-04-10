export type OrderStatus = "pending" | "confirmed" | "shipped" | "delivered" | "cancelled"

export interface Product {
  id: string
  name: string
  description?: string
  price: number
  category?: string
  is_active: boolean
  created_at: string
  updated_at: string
}

export interface Order {
  id: string
  product_id: string
  user_id: string
  status: OrderStatus
  quantity: number
  total_price: number
  created_at: string
  updated_at: string
}

export interface CreateOrderInput {
  product_id: string
  quantity: number
  metadata?: Record<string, unknown>
}
