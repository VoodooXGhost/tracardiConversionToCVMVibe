/**
 * Utility functions for formatting data display
 */

export const formatCurrency = (amount: number, currency = 'MZN'): string => {
  return new Intl.NumberFormat('pt-MZ', {
    style: 'currency',
    currency: currency,
    minimumFractionDigits: 0,
    maximumFractionDigits: 2,
  }).format(amount)
}

export const formatNumber = (num: number): string => {
  if (num >= 1000000) {
    return (num / 1000000).toFixed(1) + 'M'
  }
  if (num >= 1000) {
    return (num / 1000).toFixed(1) + 'K'
  }
  return num.toString()
}

export const formatPercentage = (num: number, decimals = 1): string => {
  return `${(num * 100).toFixed(decimals)}%`
}

export const formatDate = (date: string | Date): string => {
  const d = new Date(date)
  return d.toLocaleDateString('pt-MZ', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  })
}

export const formatDateTime = (date: string | Date): string => {
  const d = new Date(date)
  return d.toLocaleString('pt-MZ', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

export const formatPhoneNumber = (phone: string): string => {
  // Format Mozambican phone numbers
  if (phone.startsWith('+258')) {
    const number = phone.slice(4)
    if (number.length === 9) {
      return `+258 ${number.slice(0, 2)} ${number.slice(2, 5)} ${number.slice(5)}`
    }
  }
  return phone
}

export const formatDataSize = (bytes: number): string => {
  if (bytes === 0) return '0 B'
  
  const k = 1024
  const sizes = ['B', 'KB', 'MB', 'GB', 'TB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  
  return parseFloat((bytes / Math.pow(k, i)).toFixed(1)) + ' ' + sizes[i]
}

export const formatDuration = (seconds: number): string => {
  if (seconds < 60) {
    return `${seconds}s`
  } else if (seconds < 3600) {
    const minutes = Math.floor(seconds / 60)
    const remainingSeconds = seconds % 60
    return remainingSeconds > 0 ? `${minutes}m ${remainingSeconds}s` : `${minutes}m`
  } else {
    const hours = Math.floor(seconds / 3600)
    const minutes = Math.floor((seconds % 3600) / 60)
    return minutes > 0 ? `${hours}h ${minutes}m` : `${hours}h`
  }
}

export const formatRiskLevel = (level: string): { text: string; color: string } => {
  switch (level.toLowerCase()) {
    case 'high':
      return { text: 'High Risk', color: 'text-red-600 bg-red-100' }
    case 'medium':
      return { text: 'Medium Risk', color: 'text-yellow-600 bg-yellow-100' }
    case 'low':
      return { text: 'Low Risk', color: 'text-green-600 bg-green-100' }
    default:
      return { text: 'Unknown', color: 'text-gray-600 bg-gray-100' }
  }
}

export const formatCustomerType = (type: string): { text: string; color: string } => {
  switch (type.toLowerCase()) {
    case 'prepaid':
      return { text: 'Prepaid', color: 'text-blue-600 bg-blue-100' }
    case 'postpaid':
      return { text: 'Postpaid', color: 'text-purple-600 bg-purple-100' }
    default:
      return { text: type, color: 'text-gray-600 bg-gray-100' }
  }
}

export const formatStatus = (status: string): { text: string; color: string } => {
  switch (status.toLowerCase()) {
    case 'active':
      return { text: 'Active', color: 'text-green-600 bg-green-100' }
    case 'suspended':
      return { text: 'Suspended', color: 'text-yellow-600 bg-yellow-100' }
    case 'churned':
      return { text: 'Churned', color: 'text-red-600 bg-red-100' }
    case 'draft':
      return { text: 'Draft', color: 'text-gray-600 bg-gray-100' }
    case 'scheduled':
      return { text: 'Scheduled', color: 'text-blue-600 bg-blue-100' }
    case 'running':
      return { text: 'Running', color: 'text-green-600 bg-green-100' }
    case 'completed':
      return { text: 'Completed', color: 'text-purple-600 bg-purple-100' }
    case 'paused':
      return { text: 'Paused', color: 'text-yellow-600 bg-yellow-100' }
    default:
      return { text: status, color: 'text-gray-600 bg-gray-100' }
  }
}

export const getRelativeTime = (date: string | Date): string => {
  const now = new Date()
  const past = new Date(date)
  const diffInSeconds = Math.floor((now.getTime() - past.getTime()) / 1000)

  if (diffInSeconds < 60) {
    return 'just now'
  } else if (diffInSeconds < 3600) {
    const minutes = Math.floor(diffInSeconds / 60)
    return `${minutes} minute${minutes > 1 ? 's' : ''} ago`
  } else if (diffInSeconds < 86400) {
    const hours = Math.floor(diffInSeconds / 3600)
    return `${hours} hour${hours > 1 ? 's' : ''} ago`
  } else if (diffInSeconds < 2592000) {
    const days = Math.floor(diffInSeconds / 86400)
    return `${days} day${days > 1 ? 's' : ''} ago`
  } else {
    return formatDate(date)
  }
}