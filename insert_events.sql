INSERT INTO events (title, start_date, start_time, location_name, location_address, city, description, event_type, status, created_at, updated_at) 
SELECT 'Yelm Christmas in the Park Tree Lighting', '2025-11-16', '17:30', 'Yelm City Park', '105 Yelm Ave W, Yelm, WA 98597', 'Yelm', 'Join us for the annual Christmas in the Park celebration featuring tree lighting, caroling, hot cocoa, and visits with Santa.', 'Holiday', 'approved', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP 
WHERE NOT EXISTS (SELECT 1 FROM events WHERE title = 'Yelm Christmas in the Park Tree Lighting' AND start_date = '2025-11-16');
INSERT INTO events (title, start_date, start_time, location_name, location_address, city, description, event_type, status, created_at, updated_at) 
SELECT 'Olympia Harbor Days Festival', '2025-11-17', '10:00', 'Percival Landing Park', '217 Thurston Ave NW, Olympia, WA 98501', 'Olympia', 'Annual waterfront festival celebrating maritime heritage with live music, food vendors, craft booths, and kids'' activities.', 'Festival', 'approved', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP 
WHERE NOT EXISTS (SELECT 1 FROM events WHERE title = 'Olympia Harbor Days Festival' AND start_date = '2025-11-17');
INSERT INTO events (title, start_date, start_time, location_name, location_address, city, description, event_type, status, created_at, updated_at) 
SELECT 'Lacey Spring Fun Fair', '2025-11-18', '11:00', 'Regional Athletic Complex', '7600 Depot Dr SE, Lacey, WA 98503', 'Lacey', 'Community spring celebration with carnival rides, games, local vendors, live entertainment, and food trucks.', 'Festival', 'approved', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP 
WHERE NOT EXISTS (SELECT 1 FROM events WHERE title = 'Lacey Spring Fun Fair' AND start_date = '2025-11-18');
INSERT INTO events (title, start_date, start_time, location_name, location_address, city, description, event_type, status, created_at, updated_at) 
SELECT 'Tumwater Artesian Brewfest', '2025-11-19', '13:00', 'Tumwater Historical Park', '777 Simmons Rd SW, Tumwater, WA 98501', 'Tumwater', 'Annual craft beer festival featuring local and regional breweries, live music, food vendors, and artisan market.', 'Festival', 'approved', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP 
WHERE NOT EXISTS (SELECT 1 FROM events WHERE title = 'Tumwater Artesian Brewfest' AND start_date = '2025-11-19');
INSERT INTO events (title, start_date, start_time, location_name, location_address, city, description, event_type, status, created_at, updated_at) 
SELECT 'Thurston County Fair', '2025-11-20', '09:00', 'Thurston County Fairgrounds', '3054 Carpenter Rd SE, Lacey, WA 98503', 'Lacey', 'Week-long county fair with carnival rides, livestock shows, competitions, concerts, and traditional fair food.', 'Festival', 'approved', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP 
WHERE NOT EXISTS (SELECT 1 FROM events WHERE title = 'Thurston County Fair' AND start_date = '2025-11-20');
INSERT INTO events (title, start_date, start_time, location_name, location_address, city, description, event_type, status, created_at, updated_at) 
SELECT 'Olympia Farmers Market Opening Day', '2025-11-21', '10:00', 'Olympia Farmers Market', '700 Capitol Way N, Olympia, WA 98501', 'Olympia', 'Season opening of the renowned Olympia Farmers Market featuring fresh produce, artisan goods, live music, and community celebration.', 'Market', 'approved', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP 
WHERE NOT EXISTS (SELECT 1 FROM events WHERE title = 'Olympia Farmers Market Opening Day' AND start_date = '2025-11-21');
INSERT INTO events (title, start_date, start_time, location_name, location_address, city, description, event_type, status, created_at, updated_at) 
SELECT 'Procession of the Species', '2025-11-22', '16:30', 'Downtown Olympia', 'Capitol Way, Olympia, WA 98501', 'Olympia', 'Annual community celebration of Earth Day featuring a parade of giant puppets, costumes, music, and dance representing the natural world.', 'Parade', 'approved', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP 
WHERE NOT EXISTS (SELECT 1 FROM events WHERE title = 'Procession of the Species' AND start_date = '2025-11-22');
INSERT INTO events (title, start_date, start_time, location_name, location_address, city, description, event_type, status, created_at, updated_at) 
SELECT 'Lacey in Tune Summer Concert Series', '2025-11-23', '18:00', 'Huntamer Park', '1320 Ruddell Rd SE, Lacey, WA 98503', 'Lacey', 'Free outdoor concert series featuring local and regional bands across various genres. Bring blankets and picnic baskets!', 'Concert', 'approved', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP 
WHERE NOT EXISTS (SELECT 1 FROM events WHERE title = 'Lacey in Tune Summer Concert Series' AND start_date = '2025-11-23');
INSERT INTO events (title, start_date, start_time, location_name, location_address, city, description, event_type, status, created_at, updated_at) 
SELECT 'Olympia Film Festival', '2025-11-24', NULL, 'Multiple Venues', 'Downtown Olympia, WA 98501', 'Olympia', 'Week-long independent film festival showcasing local, national, and international films with Q&A sessions and filmmaker panels.', 'Film', 'approved', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP 
WHERE NOT EXISTS (SELECT 1 FROM events WHERE title = 'Olympia Film Festival' AND start_date = '2025-11-24');
INSERT INTO events (title, start_date, start_time, location_name, location_address, city, description, event_type, status, created_at, updated_at) 
SELECT 'Yelm Prairie Days', '2025-11-25', '09:00', 'Downtown Yelm', 'Yelm Ave, Yelm, WA 98597', 'Yelm', 'Annual community celebration with parade, street fair, live entertainment, food vendors, and family activities.', 'Festival', 'approved', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP 
WHERE NOT EXISTS (SELECT 1 FROM events WHERE title = 'Yelm Prairie Days' AND start_date = '2025-11-25');
INSERT INTO events (title, start_date, start_time, location_name, location_address, city, description, event_type, status, created_at, updated_at) 
SELECT 'Lakefair', '2025-11-26', '10:00', 'Capitol Lake Park', '500 Water St SW, Olympia, WA 98501', 'Olympia', 'Olympia''s premier summer festival with carnival rides, live music, food vendors, beer garden, and fireworks over Capitol Lake.', 'Festival', 'approved', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP 
WHERE NOT EXISTS (SELECT 1 FROM events WHERE title = 'Lakefair' AND start_date = '2025-11-26');
INSERT INTO events (title, start_date, start_time, location_name, location_address, city, description, event_type, status, created_at, updated_at) 
SELECT 'Tenino Oregon Trail Days', '2025-11-27', '10:00', 'City Park', '399 Park Ave E, Tenino, WA 98589', 'Tenino', 'Historical celebration featuring pioneer reenactments, vintage demonstrations, live music, food vendors, and craft fair.', 'Festival', 'approved', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP 
WHERE NOT EXISTS (SELECT 1 FROM events WHERE title = 'Tenino Oregon Trail Days' AND start_date = '2025-11-27');
INSERT INTO events (title, start_date, start_time, location_name, location_address, city, description, event_type, status, created_at, updated_at) 
SELECT 'Olympia Arts Walk', '2025-11-28', '17:00', 'Downtown Olympia', '4th Ave, Olympia, WA 98501', 'Olympia', 'Monthly evening art walk featuring galleries, studios, shops, and street performances throughout downtown.', 'Arts & Culture', 'approved', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP 
WHERE NOT EXISTS (SELECT 1 FROM events WHERE title = 'Olympia Arts Walk' AND start_date = '2025-11-28');
INSERT INTO events (title, start_date, start_time, location_name, location_address, city, description, event_type, status, created_at, updated_at) 
SELECT 'Tumwater Falls Festival', '2025-11-29', '11:00', 'Tumwater Falls Park', '110 Deschutes Way SW, Tumwater, WA 98501', 'Tumwater', 'Annual festival celebrating salmon migration with environmental exhibits, Native American cultural demonstrations, food, and music.', 'Festival', 'approved', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP 
WHERE NOT EXISTS (SELECT 1 FROM events WHERE title = 'Tumwater Falls Festival' AND start_date = '2025-11-29');
INSERT INTO events (title, start_date, start_time, location_name, location_address, city, description, event_type, status, created_at, updated_at) 
SELECT 'Rochester Community Fair', '2025-11-30', '10:00', 'Rochester Fairgrounds', '12375 183rd Ave SW, Rochester, WA 98579', 'Rochester', 'Small-town fair with demolition derby, livestock shows, carnival rides, vendor booths, and live entertainment.', 'Festival', 'approved', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP 
WHERE NOT EXISTS (SELECT 1 FROM events WHERE title = 'Rochester Community Fair' AND start_date = '2025-11-30');
INSERT INTO events (title, start_date, start_time, location_name, location_address, city, description, event_type, status, created_at, updated_at) 
SELECT 'Hands On Children''s Museum Free Day', '2025-12-01', '10:00', 'Hands On Children''s Museum', '414 Jefferson St NE, Olympia, WA 98501', 'Olympia', 'Monthly free admission day at the interactive children''s museum featuring exhibits, activities, and special programs.', 'Family', 'approved', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP 
WHERE NOT EXISTS (SELECT 1 FROM events WHERE title = 'Hands On Children''s Museum Free Day' AND start_date = '2025-12-01');
INSERT INTO events (title, start_date, start_time, location_name, location_address, city, description, event_type, status, created_at, updated_at) 
SELECT 'Olympia Symphony Orchestra Concert', '2025-12-02', '19:30', 'Washington Center for the Performing Arts', '512 Washington St SE, Olympia, WA 98501', 'Olympia', 'Professional symphony orchestra performance featuring classical and contemporary works.', 'Concert', 'approved', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP 
WHERE NOT EXISTS (SELECT 1 FROM events WHERE title = 'Olympia Symphony Orchestra Concert' AND start_date = '2025-12-02');
INSERT INTO events (title, start_date, start_time, location_name, location_address, city, description, event_type, status, created_at, updated_at) 
SELECT 'Lacey Museum Heritage Day', '2025-12-03', '12:00', 'Lacey Museum', '829 Carpenter Rd SE, Lacey, WA 98503', 'Lacey', 'Free museum open house with historical exhibits, demonstrations, activities, and local history presentations.', 'Educational', 'approved', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP 
WHERE NOT EXISTS (SELECT 1 FROM events WHERE title = 'Lacey Museum Heritage Day' AND start_date = '2025-12-03');
INSERT INTO events (title, start_date, start_time, location_name, location_address, city, description, event_type, status, created_at, updated_at) 
SELECT 'Olympia Holiday Market', '2025-12-04', '10:00', 'Greater Olympia Sports Complex', '2929 Carpenter Rd SE, Lacey, WA 98503', 'Lacey', 'Indoor holiday shopping event featuring local artisans, crafters, food vendors, and live entertainment.', 'Market', 'approved', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP 
WHERE NOT EXISTS (SELECT 1 FROM events WHERE title = 'Olympia Holiday Market' AND start_date = '2025-12-04');
INSERT INTO events (title, start_date, start_time, location_name, location_address, city, description, event_type, status, created_at, updated_at) 
SELECT 'Tumwater Community BBQ & Concert', '2025-12-05', '17:00', 'Tumwater Valley Golf Club', '4611 Tumwater Valley Dr SE, Tumwater, WA 98501', 'Tumwater', 'Independence Day celebration with BBQ dinner, live music, and fireworks display.', 'Holiday', 'approved', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP 
WHERE NOT EXISTS (SELECT 1 FROM events WHERE title = 'Tumwater Community BBQ & Concert' AND start_date = '2025-12-05');
INSERT INTO events (title, start_date, start_time, location_name, location_address, city, description, event_type, status, created_at, updated_at) 
SELECT 'Olympia Reggae Festival', '2025-12-06', '12:00', 'Brewery Park', '401 7th Ave SW, Olympia, WA 98501', 'Olympia', 'Outdoor reggae music festival featuring regional and national acts, food vendors, and beer garden.', 'Concert', 'approved', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP 
WHERE NOT EXISTS (SELECT 1 FROM events WHERE title = 'Olympia Reggae Festival' AND start_date = '2025-12-06');
INSERT INTO events (title, start_date, start_time, location_name, location_address, city, description, event_type, status, created_at, updated_at) 
SELECT 'Lacey Harvest Festival', '2025-12-07', '10:00', 'Long Lake Ranch', '4915 Yelm Hwy SE, Lacey, WA 98503', 'Lacey', 'Fall celebration with pumpkin patch, corn maze, hayrides, petting zoo, and autumn-themed activities.', 'Festival', 'approved', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP 
WHERE NOT EXISTS (SELECT 1 FROM events WHERE title = 'Lacey Harvest Festival' AND start_date = '2025-12-07');
INSERT INTO events (title, start_date, start_time, location_name, location_address, city, description, event_type, status, created_at, updated_at) 
SELECT 'Olympia Comic Con', '2025-12-08', '10:00', 'Olympia Center', '222 Columbia St NW, Olympia, WA 98501', 'Olympia', 'Pop culture convention featuring vendors, artists, cosplay contest, panels, and special guests.', 'Convention', 'approved', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP 
WHERE NOT EXISTS (SELECT 1 FROM events WHERE title = 'Olympia Comic Con' AND start_date = '2025-12-08');
INSERT INTO events (title, start_date, start_time, location_name, location_address, city, description, event_type, status, created_at, updated_at) 
SELECT 'Yelm Winter Fest', '2025-12-09', '16:00', 'Yelm Community Center', '210 2nd St SE, Yelm, WA 98597', 'Yelm', 'Community winter celebration with holiday activities, crafts, Santa visits, and seasonal refreshments.', 'Holiday', 'approved', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP 
WHERE NOT EXISTS (SELECT 1 FROM events WHERE title = 'Yelm Winter Fest' AND start_date = '2025-12-09');
INSERT INTO events (title, start_date, start_time, location_name, location_address, city, description, event_type, status, created_at, updated_at) 
SELECT 'Olympia VegFest', '2025-12-10', '11:00', 'Olympia Center', '222 Columbia St NW, Olympia, WA 98501', 'Olympia', 'Plant-based food and lifestyle festival with vendors, cooking demos, speakers, and tastings.', 'Festival', 'approved', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP 
WHERE NOT EXISTS (SELECT 1 FROM events WHERE title = 'Olympia VegFest' AND start_date = '2025-12-10');
INSERT INTO events (title, start_date, start_time, location_name, location_address, city, description, event_type, status, created_at, updated_at) 
SELECT 'Lacey 5K Fun Run', '2025-12-11', '08:00', 'Woodland Creek Community Park', '6729 Pacific Ave SE, Lacey, WA 98503', 'Lacey', 'Community fun run/walk supporting local charities with awards, refreshments, and family activities.', 'Sports', 'approved', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP 
WHERE NOT EXISTS (SELECT 1 FROM events WHERE title = 'Lacey 5K Fun Run' AND start_date = '2025-12-11');
INSERT INTO events (title, start_date, start_time, location_name, location_address, city, description, event_type, status, created_at, updated_at) 
SELECT 'Tumwater Chocolate Festival', '2025-12-12', '10:00', 'Tumwater Community Center', '5304 Littlerock Rd SW, Tumwater, WA 98512', 'Tumwater', 'Valentine''s weekend chocolate celebration with vendors, tastings, cooking demos, and chocolate-themed activities.', 'Festival', 'approved', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP 
WHERE NOT EXISTS (SELECT 1 FROM events WHERE title = 'Tumwater Chocolate Festival' AND start_date = '2025-12-12');
INSERT INTO events (title, start_date, start_time, location_name, location_address, city, description, event_type, status, created_at, updated_at) 
SELECT 'Olympia Wooden Boat Fair', '2025-12-13', '10:00', 'Percival Landing', '217 Thurston Ave NW, Olympia, WA 98501', 'Olympia', 'Maritime celebration showcasing wooden boats, boat building demonstrations, maritime history, and waterfront activities.', 'Festival', 'approved', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP 
WHERE NOT EXISTS (SELECT 1 FROM events WHERE title = 'Olympia Wooden Boat Fair' AND start_date = '2025-12-13');
INSERT INTO events (title, start_date, start_time, location_name, location_address, city, description, event_type, status, created_at, updated_at) 
SELECT 'Rochester Egg Hunt', '2025-12-14', '10:00', 'Rochester Park', '18990 Old Hwy 99 SW, Rochester, WA 98579', 'Rochester', 'Community Easter egg hunt with age divisions, prizes, photos with the Easter Bunny, and spring activities.', 'Holiday', 'approved', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP 
WHERE NOT EXISTS (SELECT 1 FROM events WHERE title = 'Rochester Egg Hunt' AND start_date = '2025-12-14');
INSERT INTO events (title, start_date, start_time, location_name, location_address, city, description, event_type, status, created_at, updated_at) 
SELECT 'Olympia Pet Expo', '2025-12-15', '10:00', 'Greater Olympia Sports Complex', '2929 Carpenter Rd SE, Lacey, WA 98503', 'Lacey', 'Pet-friendly expo featuring vendors, demonstrations, adoptions, pet contests, and educational seminars.', 'Expo', 'approved', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP 
WHERE NOT EXISTS (SELECT 1 FROM events WHERE title = 'Olympia Pet Expo' AND start_date = '2025-12-15');
INSERT INTO events (title, start_date, start_time, location_name, location_address, city, description, event_type, status, created_at, updated_at) 
SELECT 'Lacey Spring Carnival', '2025-12-16', '12:00', 'South Sound Center', '901 Sleater Kinney Rd SE, Lacey, WA 98503', 'Lacey', 'Spring carnival with rides, games, food vendors, live entertainment, and family activities.', 'Festival', 'approved', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP 
WHERE NOT EXISTS (SELECT 1 FROM events WHERE title = 'Lacey Spring Carnival' AND start_date = '2025-12-16');
INSERT INTO events (title, start_date, start_time, location_name, location_address, city, description, event_type, status, created_at, updated_at) 
SELECT 'Tumwater Summer Concert', '2025-12-17', '18:00', 'Tumwater Town Center', '5304 Littlerock Rd SW, Tumwater, WA 98512', 'Tumwater', 'Free outdoor concert featuring local bands, food vendors, and community gathering.', 'Concert', 'approved', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP 
WHERE NOT EXISTS (SELECT 1 FROM events WHERE title = 'Tumwater Summer Concert' AND start_date = '2025-12-17');
INSERT INTO events (title, start_date, start_time, location_name, location_address, city, description, event_type, status, created_at, updated_at) 
SELECT 'Olympia Craft Beer Week', '2025-12-18', NULL, 'Multiple Breweries', 'Various Locations, Olympia, WA 98501', 'Olympia', 'Week-long celebration of local craft beer with special releases, brewery tours, tastings, and beer-themed events.', 'Festival', 'approved', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP 
WHERE NOT EXISTS (SELECT 1 FROM events WHERE title = 'Olympia Craft Beer Week' AND start_date = '2025-12-18');
INSERT INTO events (title, start_date, start_time, location_name, location_address, city, description, event_type, status, created_at, updated_at) 
SELECT 'Yelm Pumpkin Run', '2025-12-19', '09:00', 'Yelm City Park', '105 Yelm Ave W, Yelm, WA 98597', 'Yelm', 'Fall-themed 5K run/walk with costume contest, post-race refreshments, and autumn activities for all ages.', 'Sports', 'approved', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP 
WHERE NOT EXISTS (SELECT 1 FROM events WHERE title = 'Yelm Pumpkin Run' AND start_date = '2025-12-19');
INSERT INTO events (title, start_date, start_time, location_name, location_address, city, description, event_type, status, created_at, updated_at) 
SELECT 'Olympia Holiday Lights Parade', '2025-12-20', '17:30', 'Downtown Olympia', 'Capitol Way, Olympia, WA 98501', 'Olympia', 'Annual lighted holiday parade with floats, marching bands, community groups, and Santa Claus finale.', 'Parade', 'approved', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP 
WHERE NOT EXISTS (SELECT 1 FROM events WHERE title = 'Olympia Holiday Lights Parade' AND start_date = '2025-12-20');
INSERT INTO events (title, start_date, start_time, location_name, location_address, city, description, event_type, status, created_at, updated_at) 
SELECT 'Lacey New Year''s Eve Celebration', '2025-12-21', '20:00', 'Regional Athletic Complex', '7600 Depot Dr SE, Lacey, WA 98503', 'Lacey', 'Family-friendly New Year''s Eve event with early countdown for kids, live entertainment, food, and midnight fireworks.', 'Holiday', 'approved', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP 
WHERE NOT EXISTS (SELECT 1 FROM events WHERE title = 'Lacey New Year''s Eve Celebration' AND start_date = '2025-12-21');
INSERT INTO events (title, start_date, start_time, location_name, location_address, city, description, event_type, status, created_at, updated_at) 
SELECT 'Olympia Winter Brewfest', '2025-12-22', '13:00', 'Capitol Theater', '206 5th Ave SE, Olympia, WA 98501', 'Olympia', 'Indoor winter beer festival featuring local breweries, food pairings, live music, and special winter beer releases.', 'Festival', 'approved', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP 
WHERE NOT EXISTS (SELECT 1 FROM events WHERE title = 'Olympia Winter Brewfest' AND start_date = '2025-12-22');
