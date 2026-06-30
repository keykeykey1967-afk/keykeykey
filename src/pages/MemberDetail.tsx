import { useParams, Link } from 'react-router-dom'
import { members } from '../data/members'
import Avatar from '../components/Avatar'

export default function MemberDetail() {
  const { id } = useParams<{ id: string }>()
  const member = members.find((m) => m.id === id)

  if (!member) {
    return (
      <div className="max-w-2xl mx-auto px-4 py-16 text-center">
        <div className="text-5xl mb-3">😕</div>
        <h2 className="text-xl font-bold mb-2">メンバーが見つかりません</h2>
        <Link to="/members" className="text-blue-600 hover:underline">
          ← メンバー一覧に戻る
        </Link>
      </div>
    )
  }

  return (
    <div className="max-w-2xl mx-auto px-4 py-8">
      <Link
        to="/members"
        className="text-blue-600 hover:underline text-sm mb-6 inline-block"
      >
        ← メンバー一覧に戻る
      </Link>

      <div className="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden">
        {/* Header */}
        <div className="bg-gradient-to-r from-blue-800 to-blue-600 p-8 flex items-center gap-5">
          <Avatar initials={member.avatar} size="lg" id={member.id} />
          <div className="text-white">
            <h1 className="text-2xl font-bold">{member.name}</h1>
            <p className="text-blue-200 text-sm">{member.nameKana}</p>
            <div className="flex flex-wrap gap-2 mt-2">
              <span className="bg-blue-700 text-blue-100 text-xs px-3 py-1 rounded-full">
                {member.graduationYear}年卒
              </span>
              <span className="bg-blue-700 text-blue-100 text-xs px-3 py-1 rounded-full">
                {member.department}
              </span>
            </div>
          </div>
        </div>

        {/* Body */}
        <div className="p-6 space-y-5">
          {/* Bio */}
          <div>
            <h2 className="text-sm font-semibold text-gray-400 uppercase tracking-wide mb-2">
              自己紹介
            </h2>
            <p className="text-gray-700 leading-relaxed">{member.bio}</p>
          </div>

          <hr className="border-gray-100" />

          {/* Details */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <InfoItem icon="💼" label="職業" value={member.currentJob} />
            <InfoItem icon="🏢" label="会社・組織" value={member.company} />
            <InfoItem icon="📍" label="居住地" value={member.location} />
            <InfoItem icon="📧" label="メール" value={member.email} />
          </div>

          <hr className="border-gray-100" />

          <div className="text-xs text-gray-400">
            登録日:{' '}
            {new Date(member.joinedAt).toLocaleDateString('ja-JP', {
              year: 'numeric',
              month: 'long',
              day: 'numeric',
            })}
          </div>
        </div>

        {/* Actions */}
        <div className="px-6 pb-6 flex gap-3">
          <a
            href={`mailto:${member.email}`}
            className="flex-1 text-center bg-blue-600 text-white py-2.5 rounded-lg font-semibold hover:bg-blue-700 transition-colors text-sm"
          >
            メッセージを送る
          </a>
          <button className="px-4 py-2.5 border border-gray-200 rounded-lg text-gray-600 hover:bg-gray-50 transition-colors text-sm">
            プロフィールを共有
          </button>
        </div>
      </div>
    </div>
  )
}

function InfoItem({
  icon,
  label,
  value,
}: {
  icon: string
  label: string
  value: string
}) {
  return (
    <div className="flex items-start gap-2.5">
      <span className="text-lg">{icon}</span>
      <div>
        <div className="text-xs text-gray-400">{label}</div>
        <div className="text-gray-800 font-medium text-sm">{value}</div>
      </div>
    </div>
  )
}
