import { useState } from 'react'
import { Link } from 'react-router-dom'
import { members, departments, graduationYears } from '../data/members'
import Avatar from '../components/Avatar'

export default function Members() {
  const [search, setSearch] = useState('')
  const [selectedDept, setSelectedDept] = useState('全学部')
  const [selectedYear, setSelectedYear] = useState('')

  const filtered = members.filter((m) => {
    const matchesSearch =
      !search ||
      m.name.includes(search) ||
      m.nameKana.includes(search) ||
      m.currentJob.includes(search) ||
      m.company.includes(search)
    const matchesDept =
      selectedDept === '全学部' || m.department.startsWith(selectedDept)
    const matchesYear =
      !selectedYear || m.graduationYear === parseInt(selectedYear, 10)
    return matchesSearch && matchesDept && matchesYear
  })

  return (
    <div className="max-w-6xl mx-auto px-4 py-8">
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-gray-900 mb-1">メンバー一覧</h1>
        <p className="text-gray-500">
          {members.length}名の卒業生が登録されています
        </p>
      </div>

      {/* Filters */}
      <div className="bg-white rounded-xl p-4 shadow-sm border border-gray-100 mb-6 flex flex-col md:flex-row gap-3">
        <input
          type="text"
          placeholder="名前・会社・職業で検索..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          className="flex-1 border border-gray-200 rounded-lg px-4 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-400"
        />
        <select
          value={selectedDept}
          onChange={(e) => setSelectedDept(e.target.value)}
          className="border border-gray-200 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-400 bg-white"
        >
          {departments.map((d) => (
            <option key={d} value={d}>
              {d}
            </option>
          ))}
        </select>
        <select
          value={selectedYear}
          onChange={(e) => setSelectedYear(e.target.value)}
          className="border border-gray-200 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-400 bg-white"
        >
          <option value="">全卒業年度</option>
          {graduationYears.map((y) => (
            <option key={y} value={y}>
              {y}年卒
            </option>
          ))}
        </select>
        {(search || selectedDept !== '全学部' || selectedYear) && (
          <button
            onClick={() => {
              setSearch('')
              setSelectedDept('全学部')
              setSelectedYear('')
            }}
            className="text-sm text-gray-500 hover:text-gray-800 px-3"
          >
            クリア
          </button>
        )}
      </div>

      {/* Results count */}
      <p className="text-sm text-gray-500 mb-4">
        {filtered.length}名のメンバーが見つかりました
      </p>

      {/* Member grid */}
      {filtered.length === 0 ? (
        <div className="text-center py-16 text-gray-400">
          <div className="text-5xl mb-3">🔍</div>
          <p>条件に合うメンバーが見つかりませんでした</p>
        </div>
      ) : (
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
          {filtered.map((member) => (
            <Link
              key={member.id}
              to={`/members/${member.id}`}
              className="bg-white rounded-xl p-5 shadow-sm border border-gray-100 hover:shadow-md transition-all hover:-translate-y-0.5 flex gap-4"
            >
              <Avatar initials={member.avatar} size="lg" id={member.id} />
              <div className="flex-1 min-w-0">
                <div className="font-semibold text-gray-900">{member.name}</div>
                <div className="text-xs text-gray-400">{member.nameKana}</div>
                <div className="mt-1.5 flex flex-wrap gap-1">
                  <span className="text-xs bg-blue-50 text-blue-700 px-2 py-0.5 rounded-full">
                    {member.graduationYear}年卒
                  </span>
                  <span className="text-xs bg-gray-50 text-gray-600 px-2 py-0.5 rounded-full">
                    {member.department.split(' ')[0]}
                  </span>
                </div>
                <div className="mt-2 text-sm text-gray-700 font-medium truncate">
                  {member.currentJob}
                </div>
                <div className="text-xs text-gray-400 truncate">
                  {member.company}
                </div>
                <div className="text-xs text-gray-400 mt-0.5">
                  📍 {member.location}
                </div>
              </div>
            </Link>
          ))}
        </div>
      )}
    </div>
  )
}
