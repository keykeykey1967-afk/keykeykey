import { Event } from '../types'

export const events: Event[] = [
  {
    id: '1',
    title: '2024年度 報友会東京支部 大会',
    date: '2024-11-23',
    time: '17:00',
    location: '東京プリンスホテル 鳳凰の間',
    description:
      '報友会東京支部の年次大会です。今年は卒業10周年、20周年、30周年の節目の方々を特に歓迎します。懐かしい仲間たちと再会し、近況報告や交流を深めましょう。会費には料理・飲み放題が含まれます。',
    capacity: 200,
    attendees: 143,
    category: 'reunion',
    image: '🎉',
    organizer: '報友会東京支部 事務局',
  },
  {
    id: '2',
    title: 'キャリア交流セミナー「各業界の最前線」',
    date: '2024-09-14',
    time: '14:00',
    location: 'オンライン（Zoom）',
    description:
      'IT、医療、金融、教育など各業界で活躍する卒業生が登壇し、それぞれのキャリアパスや業界の最新動向を語ります。学生・若手社会人に特におすすめです。',
    capacity: 100,
    attendees: 67,
    category: 'seminar',
    image: '💼',
    organizer: '田中 健一',
  },
  {
    id: '3',
    title: '夏の報友会BBQ大会',
    date: '2024-08-10',
    time: '11:00',
    location: '○○公園 バーベキューエリア',
    description:
      '夏恒例のBBQパーティー！家族・お子様もお気軽にご参加ください。スポーツコーナーや子ども向けゲームコーナーも設ける予定です。',
    capacity: 80,
    attendees: 80,
    category: 'party',
    image: '🍖',
    organizer: '佐藤 美咲',
  },
  {
    id: '4',
    title: '報友会ゴルフコンペ',
    date: '2024-10-05',
    time: '08:00',
    location: '○○カントリークラブ',
    description:
      '毎年恒例のゴルフコンペ。初心者から上級者まで参加歓迎。成績に関わらずみんなで楽しみましょう！参加費にはプレー代・昼食代が含まれます。',
    capacity: 40,
    attendees: 28,
    category: 'sports',
    image: '⛳',
    organizer: '中村 智行',
  },
  {
    id: '5',
    title: '卒業25周年同期会（1999年卒）',
    date: '2024-11-02',
    time: '18:30',
    location: '銀座 料亭 松の間',
    description:
      '卒業25周年を記念した同期会です。1999年卒業の皆さん、25年ぶりの再会を楽しみましょう。二次会の予定もあります。',
    capacity: 50,
    attendees: 32,
    category: 'reunion',
    image: '🥂',
    organizer: '加藤 亮',
  },
  {
    id: '6',
    title: '起業家交流ミートアップ',
    date: '2024-09-28',
    time: '19:00',
    location: '渋谷 コワーキングスペース BASE',
    description:
      '卒業生起業家たちが集まり、ビジネスの悩みや成功体験を共有するカジュアルな交流会。起業に興味のある方もぜひご参加ください。',
    capacity: 30,
    attendees: 19,
    category: 'seminar',
    image: '🚀',
    organizer: '渡辺 彩花',
  },
]

export const categoryLabels: Record<Event['category'], string> = {
  reunion: '同窓会',
  seminar: 'セミナー',
  party: 'パーティー',
  sports: 'スポーツ',
}

export const categoryColors: Record<Event['category'], string> = {
  reunion: 'bg-blue-100 text-blue-800',
  seminar: 'bg-green-100 text-green-800',
  party: 'bg-yellow-100 text-yellow-800',
  sports: 'bg-orange-100 text-orange-800',
}
