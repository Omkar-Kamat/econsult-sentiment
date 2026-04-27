import { NavLink } from 'react-router-dom'
import {
  LayoutDashboard,
  MessageSquareWarning,
  Network,
  FlaskConical,
  History,
  Cpu,
} from 'lucide-react'
import { clsx } from 'clsx'

const NAV_ITEMS = [
  { to: '/',         icon: LayoutDashboard,      label: 'Dashboard' },
  { to: '/bot',      icon: MessageSquareWarning,  label: 'Complaint Bot' },
  { to: '/clusters', icon: Network,               label: 'Clusters' },
  { to: '/insights', icon: FlaskConical,           label: 'Insights' },
  { to: '/history',  icon: History,               label: 'History' },
]

export default function Sidebar() {
  return (
    <aside className="flex flex-col w-60 min-h-screen bg-bg-surface border-r border-border shrink-0">

      {/* Logo */}
      <div className="flex items-center gap-3 px-6 py-5 border-b border-border">
        <div className="w-8 h-8 rounded bg-accent flex items-center justify-center">
          <Cpu size={16} className="text-bg" />
        </div>
        <div>
          <p className="font-display text-sm font-medium text-text-primary tracking-wider">
            COMPLAINTIQ
          </p>
          <p className="font-display text-[10px] text-text-muted tracking-widest uppercase">
            v1.0.0
          </p>
        </div>
      </div>

      {/* Navigation */}
      <nav className="flex flex-col gap-1 px-3 py-4 flex-1">
        {NAV_ITEMS.map(({ to, icon: Icon, label }) => (
          <NavLink
            key={to}
            to={to}
            end={to === '/'}
            className={({ isActive }) =>
              clsx(
                'flex items-center gap-3 px-3 py-2.5 rounded-md text-sm transition-all duration-150',
                isActive
                  ? 'bg-accent-glow text-accent border border-accent/20 font-medium'
                  : 'text-text-secondary hover:text-text-primary hover:bg-bg-raised'
              )
            }
          >
            {({ isActive }) => (
              <>
                <Icon size={16} className={isActive ? 'text-accent' : ''} />
                <span className="font-body">{label}</span>
              </>
            )}
          </NavLink>
        ))}
      </nav>

      {/* ML Status indicator at the bottom */}
      <div className="px-4 py-4 border-t border-border">
        <div className="flex items-center gap-2 px-3 py-2 rounded-md bg-bg-raised">
          <span className="w-2 h-2 rounded-full bg-sentiment-positive animate-pulse-slow" />
          <span className="font-display text-[11px] text-text-muted tracking-wide">
            ML PIPELINE READY
          </span>
        </div>
      </div>
    </aside>
  )
}