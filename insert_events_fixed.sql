INSERT INTO events (title, start_date, start_time, location, street, city, state, description, category, status, created_at) VALUES 
('Yelm Christmas in the Park Tree Lighting', '2025-11-16', '17:30', 'Yelm City Park', '105 Yelm Ave W', 'Yelm', 'WA', 'Join us for the annual Christmas in the Park celebration featuring tree lighting, caroling, hot cocoa, and visits with Santa.', 'Holiday', 'approved', CURRENT_TIMESTAMP)
ON CONFLICT (title, start_date) DO NOTHING;
INSERT INTO events (title, start_date, start_time, location, street, city, state, description, category, status, created_at) VALUES 
('Olympia Harbor Days Festival', '2025-11-17', '10:00', 'Percival Landing Park', '217 Thurston Ave NW', 'Olympia', 'WA', 'Annual waterfront festival celebrating maritime heritage with live music, food vendors, craft booths, and kids'' activities.', 'Festival', 'approved', CURRENT_TIMESTAMP)
ON CONFLICT (title, start_date) DO NOTHING;
INSERT INTO events (title, start_date, start_time, location, street, city, state, description, category, status, created_at) VALUES 
('Lacey Spring Fun Fair', '2025-11-18', '11:00', 'Regional Athletic Complex', '7600 Depot Dr SE', 'Lacey', 'WA', 'Community spring celebration with carnival rides, games, local vendors, live entertainment, and food trucks.', 'Festival', 'approved', CURRENT_TIMESTAMP)
ON CONFLICT (title, start_date) DO NOTHING;
INSERT INTO events (title, start_date, start_time, location, street, city, state, description, category, status, created_at) VALUES 
('Tumwater Artesian Brewfest', '2025-11-19', '13:00', 'Tumwater Historical Park', '777 Simmons Rd SW', 'Tumwater', 'WA', 'Annual craft beer festival featuring local and regional breweries, live music, food vendors, and artisan market.', 'Festival', 'approved', CURRENT_TIMESTAMP)
ON CONFLICT (title, start_date) DO NOTHING;
INSERT INTO events (title, start_date, start_time, location, street, city, state, description, category, status, created_at) VALUES 
('Thurston County Fair', '2025-11-20', '09:00', 'Thurston County Fairgrounds', '3054 Carpenter Rd SE', 'Lacey', 'WA', 'Week-long county fair with carnival rides, livestock shows, competitions, concerts, and traditional fair food.', 'Festival', 'approved', CURRENT_TIMESTAMP)
ON CONFLICT (title, start_date) DO NOTHING;
INSERT INTO events (title, start_date, start_time, location, street, city, state, description, category, status, created_at) VALUES 
('Olympia Farmers Market Opening Day', '2025-11-21', '10:00', 'Olympia Farmers Market', '700 Capitol Way N', 'Olympia', 'WA', 'Season opening of the renowned Olympia Farmers Market featuring fresh produce, artisan goods, live music, and community celebration.', 'Market', 'approved', CURRENT_TIMESTAMP)
ON CONFLICT (title, start_date) DO NOTHING;
INSERT INTO events (title, start_date, start_time, location, street, city, state, description, category, status, created_at) VALUES 
('Procession of the Species', '2025-11-22', '16:30', 'Downtown Olympia', 'Capitol Way', 'Olympia', 'WA', 'Annual community celebration of Earth Day featuring a parade of giant puppets, costumes, music, and dance representing the natural world.', 'Parade', 'approved', CURRENT_TIMESTAMP)
ON CONFLICT (title, start_date) DO NOTHING;
INSERT INTO events (title, start_date, start_time, location, street, city, state, description, category, status, created_at) VALUES 
('Lacey in Tune Summer Concert Series', '2025-11-23', '18:00', 'Huntamer Park', '1320 Ruddell Rd SE', 'Lacey', 'WA', 'Free outdoor concert series featuring local and regional bands across various genres. Bring blankets and picnic baskets!', 'Concert', 'approved', CURRENT_TIMESTAMP)
ON CONFLICT (title, start_date) DO NOTHING;
INSERT INTO events (title, start_date, start_time, location, street, city, state, description, category, status, created_at) VALUES 
('Olympia Film Festival', '2025-11-24', NULL, 'Multiple Venues', 'Downtown Olympia', 'Olympia', 'WA', 'Week-long independent film festival showcasing local, national, and international films with Q&A sessions and filmmaker panels.', 'Film', 'approved', CURRENT_TIMESTAMP)
ON CONFLICT (title, start_date) DO NOTHING;
INSERT INTO events (title, start_date, start_time, location, street, city, state, description, category, status, created_at) VALUES 
('Yelm Prairie Days', '2025-11-25', '09:00', 'Downtown Yelm', 'Yelm Ave', 'Yelm', 'WA', 'Annual community celebration with parade, street fair, live entertainment, food vendors, and family activities.', 'Festival', 'approved', CURRENT_TIMESTAMP)
ON CONFLICT (title, start_date) DO NOTHING;
INSERT INTO events (title, start_date, start_time, location, street, city, state, description, category, status, created_at) VALUES 
('Lakefair', '2025-11-26', '10:00', 'Capitol Lake Park', '500 Water St SW', 'Olympia', 'WA', 'Olympia''s premier summer festival with carnival rides, live music, food vendors, beer garden, and fireworks over Capitol Lake.', 'Festival', 'approved', CURRENT_TIMESTAMP)
ON CONFLICT (title, start_date) DO NOTHING;
INSERT INTO events (title, start_date, start_time, location, street, city, state, description, category, status, created_at) VALUES 
('Tenino Oregon Trail Days', '2025-11-27', '10:00', 'City Park', '399 Park Ave E', 'Tenino', 'WA', 'Historical celebration featuring pioneer reenactments, vintage demonstrations, live music, food vendors, and craft fair.', 'Festival', 'approved', CURRENT_TIMESTAMP)
ON CONFLICT (title, start_date) DO NOTHING;
INSERT INTO events (title, start_date, start_time, location, street, city, state, description, category, status, created_at) VALUES 
('Olympia Arts Walk', '2025-11-28', '17:00', 'Downtown Olympia', '4th Ave', 'Olympia', 'WA', 'Monthly evening art walk featuring galleries, studios, shops, and street performances throughout downtown.', 'Arts & Culture', 'approved', CURRENT_TIMESTAMP)
ON CONFLICT (title, start_date) DO NOTHING;
INSERT INTO events (title, start_date, start_time, location, street, city, state, description, category, status, created_at) VALUES 
('Tumwater Falls Festival', '2025-11-29', '11:00', 'Tumwater Falls Park', '110 Deschutes Way SW', 'Tumwater', 'WA', 'Annual festival celebrating salmon migration with environmental exhibits, Native American cultural demonstrations, food, and music.', 'Festival', 'approved', CURRENT_TIMESTAMP)
ON CONFLICT (title, start_date) DO NOTHING;
INSERT INTO events (title, start_date, start_time, location, street, city, state, description, category, status, created_at) VALUES 
('Rochester Community Fair', '2025-11-30', '10:00', 'Rochester Fairgrounds', '12375 183rd Ave SW', 'Rochester', 'WA', 'Small-town fair with demolition derby, livestock shows, carnival rides, vendor booths, and live entertainment.', 'Festival', 'approved', CURRENT_TIMESTAMP)
ON CONFLICT (title, start_date) DO NOTHING;
INSERT INTO events (title, start_date, start_time, location, street, city, state, description, category, status, created_at) VALUES 
('Hands On Children''s Museum Free Day', '2025-12-01', '10:00', 'Hands On Children''s Museum', '414 Jefferson St NE', 'Olympia', 'WA', 'Monthly free admission day at the interactive children''s museum featuring exhibits, activities, and special programs.', 'Family', 'approved', CURRENT_TIMESTAMP)
ON CONFLICT (title, start_date) DO NOTHING;
INSERT INTO events (title, start_date, start_time, location, street, city, state, description, category, status, created_at) VALUES 
('Olympia Symphony Orchestra Concert', '2025-12-02', '19:30', 'Washington Center for the Performing Arts', '512 Washington St SE', 'Olympia', 'WA', 'Professional symphony orchestra performance featuring classical and contemporary works.', 'Concert', 'approved', CURRENT_TIMESTAMP)
ON CONFLICT (title, start_date) DO NOTHING;
INSERT INTO events (title, start_date, start_time, location, street, city, state, description, category, status, created_at) VALUES 
('Lacey Museum Heritage Day', '2025-12-03', '12:00', 'Lacey Museum', '829 Carpenter Rd SE', 'Lacey', 'WA', 'Free museum open house with historical exhibits, demonstrations, activities, and local history presentations.', 'Educational', 'approved', CURRENT_TIMESTAMP)
ON CONFLICT (title, start_date) DO NOTHING;
INSERT INTO events (title, start_date, start_time, location, street, city, state, description, category, status, created_at) VALUES 
('Olympia Holiday Market', '2025-12-04', '10:00', 'Greater Olympia Sports Complex', '2929 Carpenter Rd SE', 'Lacey', 'WA', 'Indoor holiday shopping event featuring local artisans, crafters, food vendors, and live entertainment.', 'Market', 'approved', CURRENT_TIMESTAMP)
ON CONFLICT (title, start_date) DO NOTHING;
INSERT INTO events (title, start_date, start_time, location, street, city, state, description, category, status, created_at) VALUES 
('Tumwater Community BBQ & Concert', '2025-12-05', '17:00', 'Tumwater Valley Golf Club', '4611 Tumwater Valley Dr SE', 'Tumwater', 'WA', 'Independence Day celebration with BBQ dinner, live music, and fireworks display.', 'Holiday', 'approved', CURRENT_TIMESTAMP)
ON CONFLICT (title, start_date) DO NOTHING;
INSERT INTO events (title, start_date, start_time, location, street, city, state, description, category, status, created_at) VALUES 
('Olympia Reggae Festival', '2025-12-06', '12:00', 'Brewery Park', '401 7th Ave SW', 'Olympia', 'WA', 'Outdoor reggae music festival featuring regional and national acts, food vendors, and beer garden.', 'Concert', 'approved', CURRENT_TIMESTAMP)
ON CONFLICT (title, start_date) DO NOTHING;
INSERT INTO events (title, start_date, start_time, location, street, city, state, description, category, status, created_at) VALUES 
('Lacey Harvest Festival', '2025-12-07', '10:00', 'Long Lake Ranch', '4915 Yelm Hwy SE', 'Lacey', 'WA', 'Fall celebration with pumpkin patch, corn maze, hayrides, petting zoo, and autumn-themed activities.', 'Festival', 'approved', CURRENT_TIMESTAMP)
ON CONFLICT (title, start_date) DO NOTHING;
INSERT INTO events (title, start_date, start_time, location, street, city, state, description, category, status, created_at) VALUES 
('Olympia Comic Con', '2025-12-08', '10:00', 'Olympia Center', '222 Columbia St NW', 'Olympia', 'WA', 'Pop culture convention featuring vendors, artists, cosplay contest, panels, and special guests.', 'Convention', 'approved', CURRENT_TIMESTAMP)
ON CONFLICT (title, start_date) DO NOTHING;
INSERT INTO events (title, start_date, start_time, location, street, city, state, description, category, status, created_at) VALUES 
('Yelm Winter Fest', '2025-12-09', '16:00', 'Yelm Community Center', '210 2nd St SE', 'Yelm', 'WA', 'Community winter celebration with holiday activities, crafts, Santa visits, and seasonal refreshments.', 'Holiday', 'approved', CURRENT_TIMESTAMP)
ON CONFLICT (title, start_date) DO NOTHING;
INSERT INTO events (title, start_date, start_time, location, street, city, state, description, category, status, created_at) VALUES 
('Olympia VegFest', '2025-12-10', '11:00', 'Olympia Center', '222 Columbia St NW', 'Olympia', 'WA', 'Plant-based food and lifestyle festival with vendors, cooking demos, speakers, and tastings.', 'Festival', 'approved', CURRENT_TIMESTAMP)
ON CONFLICT (title, start_date) DO NOTHING;
INSERT INTO events (title, start_date, start_time, location, street, city, state, description, category, status, created_at) VALUES 
('Lacey 5K Fun Run', '2025-12-11', '08:00', 'Woodland Creek Community Park', '6729 Pacific Ave SE', 'Lacey', 'WA', 'Community fun run/walk supporting local charities with awards, refreshments, and family activities.', 'Sports', 'approved', CURRENT_TIMESTAMP)
ON CONFLICT (title, start_date) DO NOTHING;
INSERT INTO events (title, start_date, start_time, location, street, city, state, description, category, status, created_at) VALUES 
('Tumwater Chocolate Festival', '2025-12-12', '10:00', 'Tumwater Community Center', '5304 Littlerock Rd SW', 'Tumwater', 'WA', 'Valentine''s weekend chocolate celebration with vendors, tastings, cooking demos, and chocolate-themed activities.', 'Festival', 'approved', CURRENT_TIMESTAMP)
ON CONFLICT (title, start_date) DO NOTHING;
INSERT INTO events (title, start_date, start_time, location, street, city, state, description, category, status, created_at) VALUES 
('Olympia Wooden Boat Fair', '2025-12-13', '10:00', 'Percival Landing', '217 Thurston Ave NW', 'Olympia', 'WA', 'Maritime celebration showcasing wooden boats, boat building demonstrations, maritime history, and waterfront activities.', 'Festival', 'approved', CURRENT_TIMESTAMP)
ON CONFLICT (title, start_date) DO NOTHING;
INSERT INTO events (title, start_date, start_time, location, street, city, state, description, category, status, created_at) VALUES 
('Rochester Egg Hunt', '2025-12-14', '10:00', 'Rochester Park', '18990 Old Hwy 99 SW', 'Rochester', 'WA', 'Community Easter egg hunt with age divisions, prizes, photos with the Easter Bunny, and spring activities.', 'Holiday', 'approved', CURRENT_TIMESTAMP)
ON CONFLICT (title, start_date) DO NOTHING;
INSERT INTO events (title, start_date, start_time, location, street, city, state, description, category, status, created_at) VALUES 
('Olympia Pet Expo', '2025-12-15', '10:00', 'Greater Olympia Sports Complex', '2929 Carpenter Rd SE', 'Lacey', 'WA', 'Pet-friendly expo featuring vendors, demonstrations, adoptions, pet contests, and educational seminars.', 'Expo', 'approved', CURRENT_TIMESTAMP)
ON CONFLICT (title, start_date) DO NOTHING;
INSERT INTO events (title, start_date, start_time, location, street, city, state, description, category, status, created_at) VALUES 
('Lacey Spring Carnival', '2025-12-16', '12:00', 'South Sound Center', '901 Sleater Kinney Rd SE', 'Lacey', 'WA', 'Spring carnival with rides, games, food vendors, live entertainment, and family activities.', 'Festival', 'approved', CURRENT_TIMESTAMP)
ON CONFLICT (title, start_date) DO NOTHING;
INSERT INTO events (title, start_date, start_time, location, street, city, state, description, category, status, created_at) VALUES 
('Tumwater Summer Concert', '2025-12-17', '18:00', 'Tumwater Town Center', '5304 Littlerock Rd SW', 'Tumwater', 'WA', 'Free outdoor concert featuring local bands, food vendors, and community gathering.', 'Concert', 'approved', CURRENT_TIMESTAMP)
ON CONFLICT (title, start_date) DO NOTHING;
INSERT INTO events (title, start_date, start_time, location, street, city, state, description, category, status, created_at) VALUES 
('Olympia Craft Beer Week', '2025-12-18', NULL, 'Multiple Breweries', 'Various Locations', 'Olympia', 'WA', 'Week-long celebration of local craft beer with special releases, brewery tours, tastings, and beer-themed events.', 'Festival', 'approved', CURRENT_TIMESTAMP)
ON CONFLICT (title, start_date) DO NOTHING;
INSERT INTO events (title, start_date, start_time, location, street, city, state, description, category, status, created_at) VALUES 
('Yelm Pumpkin Run', '2025-12-19', '09:00', 'Yelm City Park', '105 Yelm Ave W', 'Yelm', 'WA', 'Fall-themed 5K run/walk with costume contest, post-race refreshments, and autumn activities for all ages.', 'Sports', 'approved', CURRENT_TIMESTAMP)
ON CONFLICT (title, start_date) DO NOTHING;
INSERT INTO events (title, start_date, start_time, location, street, city, state, description, category, status, created_at) VALUES 
('Olympia Holiday Lights Parade', '2025-12-20', '17:30', 'Downtown Olympia', 'Capitol Way', 'Olympia', 'WA', 'Annual lighted holiday parade with floats, marching bands, community groups, and Santa Claus finale.', 'Parade', 'approved', CURRENT_TIMESTAMP)
ON CONFLICT (title, start_date) DO NOTHING;
INSERT INTO events (title, start_date, start_time, location, street, city, state, description, category, status, created_at) VALUES 
('Lacey New Year''s Eve Celebration', '2025-12-21', '20:00', 'Regional Athletic Complex', '7600 Depot Dr SE', 'Lacey', 'WA', 'Family-friendly New Year''s Eve event with early countdown for kids, live entertainment, food, and midnight fireworks.', 'Holiday', 'approved', CURRENT_TIMESTAMP)
ON CONFLICT (title, start_date) DO NOTHING;
INSERT INTO events (title, start_date, start_time, location, street, city, state, description, category, status, created_at) VALUES 
('Olympia Winter Brewfest', '2025-12-22', '13:00', 'Capitol Theater', '206 5th Ave SE', 'Olympia', 'WA', 'Indoor winter beer festival featuring local breweries, food pairings, live music, and special winter beer releases.', 'Festival', 'approved', CURRENT_TIMESTAMP)
ON CONFLICT (title, start_date) DO NOTHING;
