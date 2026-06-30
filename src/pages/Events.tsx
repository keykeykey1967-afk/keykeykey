import { useState } from 'react'
import { events, categoryLabels, categoryColors } from '../data/events'
import type { Event } from '../types'

export default function Events() {
  const [selectedCategory, setSelectedCategory] = useState<string>('all')
  const [selectedEvent, setSelectedEvent] = useState<Event | null>(null)

  const categories = [
    { value: 'all', label: 'すべて' },
    { value: 'reunion', label: '同窓会' },
    { value: 'seminar', label: 'セミナー' },
    { value: 'party', label: 'パーティー' },
    { value: 'sports', label: 'スポーツ' },
  ]

  const filtered =
    selectedCategory === 'all'
      ? events
      : events.filter((e) => e.category === selectedCategory)

  return (
    <div className="max-w-6xl mx-auto px-4 py-8">
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-gray-900 mb-1">イベント</h1>
        <p className="text-gray-500">
          報友会東京支部のイベント・交流会・セミナー情報
        </p>
      </div>

      {/* Category filter */}
      <div className="flex flex-wrap gap-2 mb-6">
        {categories.map((cat) => (
          <button
            key={cat.value}
            onClick={() => setSelectedCategory(cat.value)}
            className={`px-4 py-1.5 rounded-full text-sm font-medium transition-colors ${
              selectedCategory === cat.value
                ? 'bg-blue-600 text-white'
                : 'bg-white text-gray-600 border border-gray-200 hover:border-blue-300 hover:text-blue-600'
            }`}
          >
            {cat.label}
          </button>
        ))}
      </div>

      {/* Events grid */}
      <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-5">
        {filtered.map((event) => {
          const isFull = event.attendees >= event.capacity
          const fillPct = Math.min((event.attendees / event.capacity) * 100, 100)
          return (
            <div
              key={event.id}
              className="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden hover:shadow-md transition-shadow cursor-pointer"
              onClick={() => setSelectedEvent(event)}
            >
              <div className="bg-gradient-to-br from-blue-50 to-blue-100 p-6 flex items-center justify-center">
                <span className="text-5xl">{event.image}</span>
              </div>
              <div className="p-5">
                <div className="flex items-center gap-2 mb-2">
                  <span
                    className={`text-xs px-2 py-0.5 rounded-full font-medium ${categoryColors[event.category]}`}
                  >
                    {categoryLabels[event.category]}
                  </span>
                  {isFull && (
                    <span className="text-xs px-2 py-0.5 rounded-full bg-red-100 text-red-700 font-medium">
                      満員
                    </span>
                  )}
                </div>
                <h3 className="font-bold text-gray-900 mb-2 leading-tight">
                  {event.title}
                </h3>
                <div className="space-y-1 text-sm text-gray-500">
                  <div className="flex items-center gap-1.5">
                    <span>📅</span>
                    <span>
                      {new Date(event.date).toLocaleDateString('ja-JP', {
                        year: 'numeric',
                        month: 'long',
                        day: 'numeric',
                      })}{' '}
                      {event.time}
                    </span>
                  </div>
                  <div className="flex items-center gap-1.5">
                    <span>📍</span>
                    <span className="truncate">{event.location}</span>
                  </div>
                </div>

                <div className="mt-3">
                  <div className="flex justify-between text-xs text-gray-400 mb-1">
                    <span>参加者</span>
                    <span>
                      {event.attendees}/{event.capacity}名
                    </span>
                  </div>
                  <div className="bg-gray-100 rounded-full h-1.5">
                    <div
                      className={`h-1.5 rounded-full ${isFull ? 'bg-red-400' : 'bg-blue-500'}`}
                      style={{ width: `${fillPct}%` }}
                    />
                  </div>
                </div>

                <button
                  className={`mt-4 w-full py-2 rounded-lg text-sm font-semibold transition-colors ${
                    isFull
                      ? 'bg-gray-100 text-gray-400 cursor-not-allowed'
                      : 'bg-blue-600 text-white hover:bg-blue-700'
                  }`}
                  disabled={isFull}
                >
                  {isFull ? '満員です' : '参加申込'}
                </button>
              </div>
            </div>
          )
        })}
      </div>

      {/* Event detail modal */}
      {selectedEvent && (
        <div
          className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4"
          onClick={() => setSelectedEvent(null)}
        >
          <div
            className="bg-white rounded-2xl shadow-xl max-w-lg w-full max-h-[90vh] overflow-y-auto"
            onClick={(e) => e.stopPropagation()}
          >
            <div className="bg-gradient-to-br from-blue-50 to-blue-100 p-8 flex items-center justify-center rounded-t-2xl">
              <span className="text-6xl">{selectedEvent.image}</span>
            </div>
            <div className="p-6">
              <div className="flex items-center gap-2 mb-3">
                <span
                  className={`text-xs px-2 py-0.5 rounded-full font-medium ${categoryColors[selectedEvent.category]}`}
                >
                  {categoryLabels[selectedEvent.category]}
                </span>
              </div>
              <h2 className="text-xl font-bold mb-4">{selectedEvent.title}</h2>
              <div className="space-y-2 text-sm text-gray-600 mb-4">
                <div className="flex items-start gap-2">
                  <span>📅</span>
                  <span>
                    {new Date(selectedEvent.date).toLocaleDateString('ja-JP', {
                      year: 'numeric',
                      month: 'long',
                      day: 'numeric',
                    })}{' '}
                    {selectedEvent.time}
                  </span>
                </div>
                <div className="flex items-start gap-2">
                  <span>📍</span>
                  <span>{selectedEvent.location}</span>
                </div>
                <div className="flex items-start gap-2">
                  <span>👤</span>
                  <span>主催: {selectedEvent.organizer}</span>
                </div>
                <div className="flex items-start gap-2">
                  <span>👥</span>
                  <span>
                    {selectedEvent.attendees}/{selectedEvent.capacity}名参加予定
                  </span>
                </div>
              </div>
              <p className="text-sm text-gray-700 leading-relaxed mb-6">
                {selectedEvent.description}
              </p>
              <div className="flex gap-3">
                <button
                  className={`flex-1 py-2.5 rounded-lg font-semibold text-sm transition-colors ${
                    selectedEvent.attendees >= selectedEvent.capacity
                      ? 'bg-gray-100 text-gray-400 cursor-not-allowed'
                      : 'bg-blue-600 text-white hover:bg-blue-700'
                  }`}
                  disabled={selectedEvent.attendees >= selectedEvent.capacity}
                >
                  {selectedEvent.attendees >= selectedEvent.capacity
                    ? '満員です'
                    : '参加申込'}
                </button>
                <button
                  onClick={() => setSelectedEvent(null)}
                  className="px-4 py-2.5 border border-gray-200 rounded-lg text-gray-600 hover:bg-gray-50 transition-colors text-sm"
                >
                  閉じる
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
