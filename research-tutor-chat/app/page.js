// app/page.js
import ChatInterface from './components/ChatInterface';

export default function Home() {
  return (
    <main className="min-h-screen bg-gray-100">
      <ChatInterface />
    </main>
  );
}

export const metadata = {
  title: 'Research Methods Tutor',
  description: 'AI-powered tutor for Research Methods for Business Students',
};
