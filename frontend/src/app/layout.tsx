import type { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'CKPA — CRM Knowledge & Policy Assistant',
  description: 'Trợ lý tra cứu quy trình CRM nội bộ SongNhat',
}

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="vi">
      <body>{children}</body>
    </html>
  )
}
