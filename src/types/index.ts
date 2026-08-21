export interface Member {
  id: string
  name: string
  nameKana: string
  graduationYear: number
  department: string
  currentJob: string
  company: string
  location: string
  email: string
  avatar: string
  bio: string
  joinedAt: string
}

export interface Event {
  id: string
  title: string
  date: string
  time: string
  location: string
  description: string
  capacity: number
  attendees: number
  category: 'reunion' | 'seminar' | 'party' | 'sports'
  image: string
  organizer: string
}

export interface News {
  id: string
  title: string
  body: string
  author: string
  publishedAt: string
  category: 'announcement' | 'news' | 'report'
}
