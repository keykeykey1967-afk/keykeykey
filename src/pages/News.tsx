import { useState } from 'react'
import { news } from '../data/news'
import type { News as NewsType } from '../types'

const categoryConfig: Record<
  NewsType['category'],
  { label: string; color: string }
> = {
  announcement: { label: 'お知らせ', color: 'bg-red-100 text-red-700' },
  news: { label: 'ニュース', color: 'bg-blue-100 text-blue-700' },
  report: { label: '報告', color: 'bg-gray-100 text-gray-700' },
}

export default function News() {
  const [selected, setSelected] = useState<NewsType | null>(null)

  return (
    <div className="max-w-3xl mx-auto px-4 py-8">
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-gray-900 mb-1">お知らせ</h1>
        <p className="text-gray-500">報友会東京支部からの最新情報をお届けします</p>
      </div>

      <div className="space-y-4">
        {news.map((item) => {
          const cat = categoryConfig[item.category]
          return (
            <button
              key={item.id}
              onClick={() => setSelected(item)}
              className="w-full bg-white rounded-xl p-5 shadow-sm border border-gray-100 hover:shadow-md transition-shadow text-left"
            >
              <div className="flex items-center gap-2 mb-2">
                <span
                  className={`text-xs px-2 py-0.5 rounded-full font-medium ${cat.color}`}
                >
                  {cat.label}
                </span>
                <span className="text-xs text-gray-400">
                  {new Date(item.publishedAt).toLocaleDateString('ja-JP', {
                    year: 'numeric',
                    month: 'long',
                    day: 'numeric',
                  })}
                </span>
              </div>
              <h2 className="font-bold text-gray-900 mb-1.5">{item.title}</h2>
              <p className="text-sm text-gray-500 line-clamp-2">{item.body}</p>
              <div className="mt-2 text-xs text-gray-400">
                投稿者: {item.author}
              </div>
            </button>
          )
        })}
      </div>

      {/* Article detail modal */}
      {selected && (
        <div
          className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4"
          onClick={() => setSelected(null)}
        >
          <div
            className="bg-white rounded-2xl shadow-xl max-w-lg w-full max-h-[90vh] overflow-y-auto"
            onClick={(e) => e.stopPropagation()}
          >
            <div className="p-6">
              <div className="flex items-center gap-2 mb-3">
                <span
                  className={`text-xs px-2 py-0.5 rounded-full font-medium ${categoryConfig[selected.category].color}`}
                >
                  {categoryConfig[selected.category].label}
                </span>
                <span className="text-xs text-gray-400">
                  {new Date(selected.publishedAt).toLocaleDateString('ja-JP', {
                    year: 'numeric',
                    month: 'long',
                    day: 'numeric',
                  })}
                </span>
              </div>
              <h2 className="text-xl font-bold mb-4">{selected.title}</h2>
              <p className="text-gray-700 leading-relaxed">{selected.body}</p>
              <div className="mt-4 text-sm text-gray-400">
                投稿者: {selected.author}
              </div>
              <button
                onClick={() => setSelected(null)}
                className="mt-6 w-full py-2.5 border border-gray-200 rounded-lg text-gray-600 hover:bg-gray-50 transition-colors text-sm"
              >
                閉じる
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
