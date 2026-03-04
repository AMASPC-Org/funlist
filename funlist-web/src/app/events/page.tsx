
export const metadata = {
  title: 'Events | FunList.ai',
};

export default function EventsPage() {
  return (
    <div className="container">
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2rem' }}>
        <h1 style={{ fontSize: '2.5rem', fontWeight: 800, color: 'var(--text-navy)' }}>
          Upcoming Fun
        </h1>
        <div style={{ display: 'flex', gap: '1rem' }}>
          <select style={{ padding: '0.5rem 1rem', borderRadius: '8px', border: '1px solid var(--border-light)' }}>
            <option>All Types</option>
            <option>Family & Kids</option>
            <option>Community</option>
          </select>
          <select style={{ padding: '0.5rem 1rem', borderRadius: '8px', border: '1px solid var(--border-light)' }}>
            <option>Any Date</option>
            <option>This Weekend</option>
          </select>
        </div>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(350px, 1fr))', gap: '2rem' }}>
        {[1, 2, 3, 4, 5, 6].map((i) => (
          <div key={i} className="card" style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
            <div style={{ height: '180px', background: 'linear-gradient(135deg, var(--bg-warm-white), #f0e6dd)', borderRadius: '12px', display: 'flex', alignItems: 'center', justifyContent: 'center', color: 'var(--text-secondary)' }}>
              Event Image Placeholder
            </div>
            <div>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start', marginBottom: '0.5rem' }}>
                <h3 style={{ fontSize: '1.25rem', fontWeight: 700, color: 'var(--text-navy)' }}>
                  Community Gathering {i}
                </h3>
                <span style={{ background: 'var(--bg-warm-white)', padding: '0.25rem 0.5rem', borderRadius: '12px', fontSize: '0.8rem', fontWeight: 600, color: 'var(--primary-orange)' }}>
                  9.{i} Vibe Score
                </span>
              </div>
              <p style={{ color: 'var(--text-secondary)', fontSize: '0.95rem', marginBottom: '1rem' }}>
                Join us for an amazing afternoon filled with activities, local food, and great company.
              </p>
              <div style={{ display: 'flex', gap: '0.5rem', fontSize: '0.85rem', color: 'var(--text-secondary)' }}>
                <span>📅 Sat, Oct {10 + i}</span>
                <span>•</span>
                <span>📍 Central Park</span>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
