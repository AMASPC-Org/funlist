import Link from 'next/link';
import EventMap from '../components/EventMap';
import EventGrid from '../components/EventGrid';
import { fetchEventsForMap } from '../lib/api';

export default async function Home() {
  const events = await fetchEventsForMap();
  
  return (
    <div>
      {/* Hero Section */}
      <section id="hero" className="hero-section">
        <div className="hero-content">
          <h1>Find the Best Events Near You – Rated for Fun!</h1>
          <p>Discover fun-rated events in your area with AI-powered matching.</p>
        </div>
      </section>

      {/* Main Call to Action / Search Area */}
      <section className="content-section text-center py-5">
        <div className="container">
          <div className="search-container mb-4">
            <form action="/map" method="GET" className="search-form">
              <div className="input-group">
                <input type="text" name="location" className="form-control form-control-lg" placeholder="Enter any location..." />
                <button type="submit" className="btn btn-primary btn-lg">
                  Find Events
                </button>
              </div>
            </form>
            <div className="text-center mt-2 d-flex justify-content-center align-items-center" style={{ gap: '1rem' }}>
              <Link href="/map" className="btn btn-link">View Full Map</Link>
              <span className="text-muted">|</span>
              <Link href="/events" className="btn btn-link">Browse All Events</Link>
            </div>
          </div>
          <button className="btn btn-outline-primary btn-lg mt-3">
            Get My Weekly FunList
          </button>
        </div>
      </section>

      {/* Main Features Grid */}
      <div className="container my-5">
        <div className="row g-4">
          <div className="col-md-4">
            <div className="feature-box bg-light">
              <h3 style={{ color: 'var(--primary-orange)' }}>AI-Driven Curation</h3>
              <p>Our AI analyzes thousands of events to find the perfect activities that match your interests and preferences.</p>
              <Link href="/about" className="btn btn-outline-primary mt-3">Learn More</Link>
            </div>
          </div>
          <div className="col-md-4">
            <div className="feature-box bg-light">
              <h3 style={{ color: 'var(--primary-orange)' }}>Funalytics™ Score</h3>
              <p>Every event gets a Funalytics™ Score based on activities, engagement level, and attendee experience.</p>
              <a href="#fun-rating-section" className="btn btn-outline-primary mt-3">Learn More</a>
            </div>
          </div>
          <div className="col-md-4">
            <div className="feature-box bg-light">
              <h3 style={{ color: 'var(--primary-orange)' }}>List Your Event</h3>
              <p>Organize an event? Share it with our community and get discovered by fun-seeking attendees.</p>
              <Link href="/auth/signin" className="btn btn-outline-primary mt-3">Submit Event</Link>
            </div>
          </div>
        </div>
      </div>

      {/* Map Integration Section */}
      <section className="py-5 bg-white">
        <div className="container">
          <h2 className="text-center mb-4 text-primary">Explore Events Near You</h2>
          <div className="card mb-5" style={{ overflow: 'hidden' }}>
            <EventMap events={events} />
          </div>
          
          <div className="mt-5">
            <h3 className="text-center mb-4" style={{ color: 'var(--primary-orange)' }}>Upcoming Events</h3>
            <EventGrid events={events} />
          </div>
        </div>
      </section>

      {/* Personal Fun Assistant Section */}
      <section id="fun-assistant" className="fun-assistant-section py-5">
        <div className="container">
          <div className="row align-items-center">
            <div className="col-md-6 mb-4">
              <h2 className="text-primary" style={{ fontWeight: 800 }}>Your Personal Fun Assistant</h2>
              <div style={{ maxWidth: '500px' }}>
                <p className="lead mb-4">Get personalized recommendations based on your interests and preferences:</p>
                <ul className="feature-list mb-4">
                  <li>AI-powered event matching</li>
                  <li>Based on the Funalytics™ Score</li>
                  <li>Weekly personalized updates</li>
                  <li>Customized notifications</li>
                </ul>
                <Link href="/auth/signin" className="btn btn-success btn-lg">
                  Try Personal Fun Assistant Now
                </Link>
              </div>
            </div>
            <div className="col-md-6">
              <div className="chat-demo">
                <div className="chat-message user">
                  <strong>You:</strong> What fun events are happening this weekend?
                </div>
                <div className="chat-message assistant">
                  <strong>Fun Assistant:</strong> Based on your interests in music and outdoor activities, I found these events:
                  <ul style={{ margin: '0.5rem 0 0 1.5rem', padding: 0 }}>
                    <li>Saturday: Downtown Music Festival (Fun Score: ⭐⭐⭐⭐)</li>
                    <li>Sunday: Harbor Park Food & Wine (Fun Score: ⭐⭐⭐⭐⭐)</li>
                  </ul>
                </div>
                <div className="chat-message user">
                  <strong>You:</strong> Tell me more about the festival!
                </div>
                <div className="chat-message assistant mb-0">
                  <strong>Fun Assistant:</strong> The Downtown Music Festival features 3 stages, local food vendors, and interactive art installations. It matches your preference for live music!
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Funalytics Score Section */}
      <section id="fun-rating-section" className="rating-system-section py-5 bg-white">
        <div className="container text-center">
          <h2 className="mb-4 text-primary">How the Funalytics™ Score Works</h2>
          <p className="lead mb-5 text-muted">Every event is scored on a 1-10 scale based on activities, engagement level, and attendee experience:</p>
          <div className="rating-scale">
            <div className="rating-item">
              <span className="stars">⭐</span>
              <p className="mb-0 fw-bold">Basic Event</p>
            </div>
            <div className="rating-item">
              <span className="stars">⭐⭐</span>
              <p className="mb-0 fw-bold">Social Elements</p>
            </div>
            <div className="rating-item">
              <span className="stars">⭐⭐⭐</span>
              <p className="mb-0 fw-bold">Interactive</p>
            </div>
            <div className="rating-item">
              <span className="stars">⭐⭐⭐⭐</span>
              <p className="mb-0 fw-bold">Multiple Activities</p>
            </div>
            <div className="rating-item">
              <span className="stars">⭐⭐⭐⭐⭐</span>
              <p className="mb-0 fw-bold">Full Experience</p>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}
