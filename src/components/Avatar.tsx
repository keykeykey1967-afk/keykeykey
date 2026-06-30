const colors = [
  'bg-blue-500',
  'bg-green-500',
  'bg-purple-500',
  'bg-red-500',
  'bg-yellow-500',
  'bg-indigo-500',
  'bg-pink-500',
  'bg-teal-500',
]

interface AvatarProps {
  initials: string
  size?: 'sm' | 'md' | 'lg'
  id?: string
}

export default function Avatar({ initials, size = 'md', id = '0' }: AvatarProps) {
  const colorIndex = parseInt(id, 10) % colors.length
  const color = colors[colorIndex]

  const sizeClasses = {
    sm: 'w-8 h-8 text-xs',
    md: 'w-12 h-12 text-sm',
    lg: 'w-16 h-16 text-lg',
  }

  return (
    <div
      className={`${color} ${sizeClasses[size]} rounded-full flex items-center justify-center text-white font-bold flex-shrink-0`}
    >
      {initials}
    </div>
  )
}
