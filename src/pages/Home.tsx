import { Link } from 'react-router-dom'
import { members } from '../data/members'
import { events } from '../data/events'
import { news } from '../data/news'
import { categoryLabels, categoryColors } from '../data/events'
import Avatar from '../components/Avatar'

export default function Home() {
  const upcomingEvents = events
    .sort((a, b) => new Date(a.date).getTime() - new Date(b.date).getTime())
    .slice(0, 3)

  const latestNews = news.slice(0, 3)
  const recentMembers = members.slice(0, 4)

  return (
    <div className="max-w-6xl mx-auto px-4 py-8 space-y-8">
      {/* Hero */}
      <div className="bg-gradient-to-r from-blue-800 to-blue-700 rounded-2xl text-white p-8 md:p-12 relative overflow-hidden">
        <div className="absolute right-6 top-1/2 -translate-y-1/2 opacity-5 select-none pointer-events-none hidden md:block">
          <span style={{ fontSize: '180px', fontFamily: 'serif', color: '#c9a84c' }}>徳</span>
        </div>
        <div className="max-w-2xl relative">
          <div className="text-gold-400 text-sm tracking-[0.3em] mb-2 font-medium">報友会東京支部</div>
          <h1 className="text-3xl md:text-4xl font-bold mb-3">
            懐かしい仲間と、また会おう。
          </h1>
          <p className="text-blue-100 text-lg mb-6">
            報友会東京支部の会員が繋がるプラットフォームです。
            同期・先輩・後輩との交流やイベント情報をまとめて管理できます。
          </p>
          <div className="flex flex-wrap gap-3">
            <Link
              to="/members"
              className="bg-gold-500 text-white px-6 py-2.5 rounded-lg font-semibold hover:bg-gold-600 transition-colors shadow-sm"
            >
              メンバーを探す
            </Link>
            <Link
              to="/events"
              className="border border-white text-white px-6 py-2.5 rounded-lg font-semibold hover:bg-blue-700 transition-colors"
            >
              イベントを見る
            </Link>
          </div>
        </div>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        {[
          { label: '登録メンバー', value: `${members.length}名`, icon: '👥' },
          { label: '開催イベント', value: `${events.length}件`, icon: '📅' },
          { label: '卒業年度', value: '20年分', icon: '🎓' },
          { label: '学部・学科', value: '8学部', icon: '🏫' },
        ].map((stat) => (
          <div
            key={stat.label}
            className="bg-white rounded-xl p-5 shadow-sm border border-gray-100 text-center"
          >
            <div className="text-3xl mb-1">{stat.icon}</div>
            <div className="text-2xl font-bold text-blue-800">{stat.value}</div>
            <div className="text-sm text-gray-500 mt-0.5">{stat.label}</div>
          </div>
        ))}
      </div>

      <div className="grid md:grid-cols-2 gap-8">
        {/* Upcoming Events */}
        <section>
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-xl font-bold">直近のイベント</h2>
            <Link to="/events" className="text-blue-600 hover:underline text-sm">
              すべて見る →
            </Link>
          </div>
          <div className="space-y-3">
            {upcomingEvents.map((event) => (
              <div
                key={event.id}
                className="bg-white rounded-xl p-4 shadow-sm border border-gray-100 hover:shadow-md transition-shadow"
              >
                <div className="flex items-start gap-3">
                  <div className="text-3xl">{event.image}</div>
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-2 mb-1">
                      <span
                        className={`text-xs px-2 py-0.5 rounded-full font-medium ${categoryColors[event.category]}`}
                      >
                        {categoryLabels[event.category]}
                      </span>
                    </div>
                    <h3 className="font-semibold text-gray-900 truncate">
                      {event.title}
                    </h3>
                    <p className="text-sm text-gray-500 mt-0.5">
                      {new Date(event.date).toLocaleDateString('ja-JP', {
                        year: 'numeric',
                        month: 'long',
                        day: 'numeric',
                      })}{' '}
                      {event.time} ／ {event.location}
                    </p>
                    <div className="mt-2 flex items-center gap-1">
                      <div className="flex-1 bg-gray-100 rounded-full h-1.5">
                        <div
                          className="bg-blue-500 h-1.5 rounded-full"
                          style={{
                            width: `${Math.min(
                              (event.attendees / event.capacity) * 100,
                              100,
                            )}%`,
                          }}
                        />
                      </div>
                      <span className="text-xs text-gray-500 whitespace-nowrap">
                        {event.attendees}/{event.capacity}名
                      </span>
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </section>

        {/* Latest News */}
        <section>
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-xl font-bold">お知らせ</h2>
            <Link to="/news" className="text-blue-600 hover:underline text-sm">
              すべて見る →
            </Link>
          </div>
          <div className="space-y-3">
            {latestNews.map((item) => (
              <div
                key={item.id}
                className="bg-white rounded-xl p-4 shadow-sm border border-gray-100 hover:shadow-md transition-shadow"
              >
                <div className="flex items-center gap-2 mb-1.5">
                  <span
                    className={`text-xs px-2 py-0.5 rounded-full font-medium ${
                      item.category === 'announcement'
                        ? 'bg-red-100 text-red-700'
                        : item.category === 'news'
                          ? 'bg-blue-100 text-blue-700'
                          : 'bg-gray-100 text-gray-700'
                    }`}
                  >
                    {item.category === 'announcement'
                      ? 'お知らせ'
                      : item.category === 'news'
                        ? 'ニュース'
                        : '報告'}
                  </span>
                  <span className="text-xs text-gray-400">
                    {new Date(item.publishedAt).toLocaleDateString('ja-JP')}
                  </span>
                </div>
                <h3 className="font-semibold text-gray-900 leading-snug">
                  {item.title}
                </h3>
                <p className="text-sm text-gray-500 mt-1 line-clamp-2">
                  {item.body}
                </p>
              </div>
            ))}
          </div>
        </section>
      </div>

      {/* Recent Members */}
      <section>
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-xl font-bold">最近登録したメンバー</h2>
          <Link to="/members" className="text-blue-600 hover:underline text-sm">
            全員を見る →
          </Link>
        </div>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          {recentMembers.map((member) => (
            <Link
              key={member.id}
              to={`/members/${member.id}`}
              className="bg-white rounded-xl p-5 shadow-sm border border-gray-100 hover:shadow-md transition-all hover:-translate-y-0.5 text-center"
            >
              <div className="flex justify-center mb-3">
                <Avatar initials={member.avatar} size="lg" id={member.id} />
              </div>
              <div className="font-semibold text-gray-900">{member.name}</div>
              <div className="text-sm text-gray-500 mt-0.5">
                {member.graduationYear}年卒
              </div>
              <div className="text-xs text-gray-400 mt-1 truncate">
                {member.currentJob}
              </div>
            </Link>
          ))}
        </div>
      </section>
    </div>
  )
}
