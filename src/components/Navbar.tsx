import { Link, useLocation } from 'react-router-dom'

const navItems = [
  { path: '/', label: 'ホーム' },
  { path: '/members', label: 'メンバー' },
  { path: '/events', label: 'イベント' },
  { path: '/news', label: 'お知らせ' },
]

export default function Navbar() {
  const location = useLocation()

  return (
    <nav className="bg-blue-800 text-white shadow-lg">
      <div className="max-w-6xl mx-auto px-4">
        <div className="flex items-center justify-between h-16">
          <Link to="/" className="flex items-center gap-2 font-bold text-xl">
            <span className="text-2xl">🎓</span>
            <span>同窓会アプリ</span>
          </Link>
          <div className="hidden md:flex items-center gap-1">
            {navItems.map((item) => (
              <Link
                key={item.path}
                to={item.path}
                className={`px-4 py-2 rounded-lg transition-colors ${
                  location.pathname === item.path
                    ? 'bg-blue-600 text-white'
                    : 'hover:bg-blue-700 text-blue-100'
                }`}
              >
                {item.label}
              </Link>
            ))}
          </div>
          <div className="flex items-center gap-2">
            <div className="w-9 h-9 rounded-full bg-blue-600 flex items-center justify-center text-sm font-bold cursor-pointer hover:bg-blue-500 transition-colors">
              田中
            </div>
          </div>
        </div>
        <div className="md:hidden flex gap-1 pb-2">
          {navItems.map((item) => (
            <Link
              key={item.path}
              to={item.path}
              className={`flex-1 text-center px-2 py-1.5 rounded text-sm transition-colors ${
                location.pathname === item.path
                  ? 'bg-blue-600 text-white'
                  : 'hover:bg-blue-700 text-blue-100'
              }`}
            >
              {item.label}
            </Link>
          ))}
        </div>
      </div>
    </nav>
  )
}
