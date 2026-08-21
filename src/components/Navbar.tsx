import { Link, useLocation } from 'react-router-dom'

const navItems = [
  { path: '/', label: 'ホーム' },
  { path: '/members', label: 'メンバー' },
  { path: '/events', label: 'イベント' },
  { path: '/news', label: 'お知らせ' },
]

function SchoolEmblem({ size = 36 }: { size?: number }) {
  return (
    <svg width={size} height={size} viewBox="0 0 36 36" fill="none" xmlns="http://www.w3.org/2000/svg">
      <circle cx="18" cy="18" r="16" fill="#101c54" stroke="#c9a84c" strokeWidth="1.8" />
      <circle cx="18" cy="18" r="12.5" fill="none" stroke="#c9a84c" strokeWidth="0.6" opacity="0.7" />
      <text
        x="18"
        y="23.5"
        textAnchor="middle"
        fontSize="14"
        fontFamily="'Hiragino Mincho ProN', 'Yu Mincho', serif"
        fill="#c9a84c"
        fontWeight="bold"
      >
        徳
      </text>
    </svg>
  )
}

export default function Navbar() {
  const location = useLocation()

  return (
    <nav className="bg-blue-800 text-white shadow-lg">
      <div className="max-w-6xl mx-auto px-4">
        <div className="flex items-center justify-between h-16">
          <Link to="/" className="flex items-center gap-2.5 font-bold">
            <SchoolEmblem size={36} />
            <div className="leading-tight">
              <div className="text-xs text-gold-400 tracking-widest font-normal">報友会</div>
              <div className="text-base font-bold tracking-wide">東京支部</div>
            </div>
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
