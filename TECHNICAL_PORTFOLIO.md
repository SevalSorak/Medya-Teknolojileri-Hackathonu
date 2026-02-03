# ANADOLU: HABER ZAMAN TÜNELİ - Technical Portfolio

## Project Summary

A hackathon-winning interactive web application that transforms how users consume news by presenting Anadolu Agency (AA) news articles through an immersive 3D art gallery experience. Users select a historical date and navigate a three.js-powered virtual gallery where news stories are displayed as crystal panels on walls. The system integrates AI-powered text summarization, text-to-speech narration using ElevenLabs API, automated video highlight generation with GPT-4, and historical news scraping from Wayback Machine archives. The project combines Python backend services for data processing with a browser-based 3D frontend for exploration.

## Tech Stack

### Backend
- **Language**: Python 3.x
- **Web Framework**: Flask (with Flask-CORS for cross-origin requests)
- **Web Scraping**: 
  - `requests` with retry mechanism (urllib3.Retry, HTTPAdapter)
  - `BeautifulSoup4` for HTML parsing
  - `feedparser` for RSS feed processing
- **Natural Language Processing**:
  - `transformers` (Hugging Face) with `nicktimur/mt5-base-turkish-news-summarizer` model
  - `openai` Python SDK for GPT-4o-mini and GPT-4 models
- **Video Processing**:
  - `ffmpeg` for audio extraction
  - `faster-whisper` for speech-to-text transcription
  - `moviepy` (VideoFileClip, concatenate_videoclips, CompositeVideoClip, ImageClip)
- **Text-to-Speech**: `elevenlabs` Python SDK
- **Image Processing**: `Pillow` (PIL) for subtitle image generation
- **Utilities**: 
  - `python-dotenv` for environment variable management
  - `numpy` for video frame operations
- **Data Storage**: JSON files (`data.json`, `summarized_data.json`, `aa_cdx_verileri.json`)

### Frontend
- **3D Graphics**: three.js (WebGL-based 3D rendering)
- **Core Technologies**: HTML5, CSS3, JavaScript (ES6+)
- **Fonts**: Google Fonts (Cinzel, IM Fell English, Crimson Text, Space Grotesk)
- **Styling**: Custom CSS with animations, glassmorphism effects, and responsive design

### External APIs & Services
- **Wayback Machine CDX API** (archive.org) for historical news retrieval
- **Anadolu Agency RSS Feeds** for current news
- **OpenAI API**: GPT-4o-mini (summarization refinement), GPT-4 (video highlight selection)
- **ElevenLabs API**: Text-to-speech synthesis
- **HTTP Server**: Development server (npx http-server or any static file server)

## Architecture & Design

### System Architecture

The application follows a decoupled client-server architecture with three main layers:

#### 1. Data Collection Layer (Offline Processing)
- **Wayback Machine Scraper** (`aa_scraping.py`): Queries CDX API with pagination support across multiple news categories (dunya, gundem, ekonomi, haberler). Implements retry logic with exponential backoff, fallback to Availability API when primary snapshot fails, and rate limiting (2-second delays). Extracts news metadata including title, content, date, category, images, and summaries using CSS selectors.
- **RSS Scraper** (`rss_scraping.py`): Fetches current news from 9 AA category feeds (guncel, ekonomi, spor, dunya, teknoloji, politika, kultur-sanat, yasam, saglik). Outputs structured CSV format for easy integration.

#### 2. Data Processing Layer (Offline NLP)
- **Summarization Pipeline** (`summarized_data.py`): 
  - Sentence tokenization and cleaning (regex-based)
  - Per-sentence summarization using mT5-based Turkish model
  - Duplicate detection via Jaccard similarity scoring
  - Quality filtering (minimum length, special character ratio checks)
  - GPT-4o-mini post-processing for fluency enhancement
  - Batch processing with progress logging
- **Video Highlight Generator** (`generate_video_shorts.py`):
  - Audio extraction using ffmpeg at 16kHz mono
  - Speech-to-text with faster-whisper (small model, CUDA-enabled)
  - GPT-4 critical segment selection based on transcript context
  - Automated subtitle generation with PIL (outlined text rendering)
  - Multi-clip concatenation with moviepy
  - Title generation using GPT-4

#### 3. Runtime Services Layer
- **TTS API Server** (`voice.py`): Flask REST endpoint (`/api/tts`) that proxies requests to ElevenLabs API. Accepts text payload, returns MP3 audio stream. CORS-enabled for specified origins. Configured with voice stability (0.4) and similarity boost (0.9) parameters.

#### 4. Presentation Layer (Browser)
- **Landing Page** (`index.html`): Period-themed UI with animated background, date picker with visual era indicators (1980s cassettes, 1990s diskettes, 2000s CDs, 2010s+ smartphones). CSS animations simulate newspaper aging effect.
- **3D Gallery** (`gallery.html`):
  - **Scene Setup**: three.js PerspectiveCamera, WebGLRenderer with shadows, ambient + directional lighting
  - **Gallery Structure**: Room system with walls, floor, ceiling using BoxGeometry. Multiple interconnected rooms for category segregation (main hall + category-specific rooms)
  - **News Display**: Crystal-like panels (PlaneGeometry with semi-transparent MeshPhysicalMaterial) positioned on walls. Each panel stores news metadata and responds to raycasting clicks
  - **NPCs (Non-Player Characters)**: Procedurally modeled humanoid figures with walk animations, idle behavior, collision detection, and category-specific dialogue bubbles
  - **Camera Controls**: First-person WASD movement, mouse look (pointer lock API), collision detection against walls
  - **Modal System**: News detail view with image display, full text, TTS button triggering API call
  - **Data Fetching**: Loads `mockNews.json` or `summarized_data.json` filtered by selected date

### Data Flow

1. **Historical Data**: Wayback Machine → `aa_scraping.py` → `aa_cdx_verileri.json` → `summarized_data.py` → `summarized_data.json`
2. **Current Data**: RSS Feeds → `rss_scraping.py` → `aa_haberler.csv`
3. **User Experience**: Date Selection (index.html) → URL Parameter → Gallery Loading (gallery.html) → Date-filtered News Display → 3D Interaction → Modal Detail View
4. **TTS Flow**: User Click → Frontend Fetch → `voice.py` → ElevenLabs API → Audio Playback

### Key Design Decisions

- **Offline-first data processing**: NLP summarization and video generation run as batch scripts rather than real-time to avoid API rate limits and reduce latency
- **JSON-based storage**: Simple file-based persistence suitable for hackathon scope, enables easy inspection/debugging
- **Client-side 3D rendering**: Leverages browser GPU acceleration via WebGL, no server-side rendering needed
- **Stateless TTS proxy**: Flask server acts as thin wrapper to hide API keys and enable CORS
- **Category-based room system**: Spatial segregation improves content discovery and creates thematic exploration zones
- **NPC integration**: Adds liveliness to static gallery environment, provides contextual category commentary

## Core Features

- **Interactive 3D News Gallery**: Navigate a three.js-powered virtual museum with WASD keyboard controls and mouse look
- **Historical Date Selection**: Access news from any date with themed UI elements representing different technological eras
- **Wayback Machine Integration**: Scrapes archived AA news articles from 2010-2025 across multiple categories
- **AI-Powered Text Summarization**: Two-stage process using mT5-based Turkish model + GPT-4o-mini refinement
- **Text-to-Speech Narration**: Natural-sounding Turkish voice synthesis via ElevenLabs API with configurable voice parameters
- **Automated Video Shorts Generation**: GPT-4 analyzes video transcripts to identify key moments, creates subtitled highlight reels
- **RSS Feed Aggregation**: Fetches current news from 9 AA category feeds
- **Crystal Panel News Display**: Semi-transparent 3D planes with news metadata rendered as interactive gallery exhibits
- **Category-Specific Rooms**: Dedicated gallery spaces for different news categories with transition doors
- **Animated NPCs**: Non-player characters with walking animations, idle behaviors, collision avoidance, and contextual dialogue
- **Modal News Details**: Full article view with title, image, complete text, and TTS playback button
- **Date-Filtered Content**: Dynamically loads news articles matching user-selected date
- **Responsive UI**: Glassmorphism design with HUD controls, category filters, and loading states
- **Error Handling**: Retry mechanisms for web scraping, fallback snapshot retrieval, quality filtering for summaries

## Algorithms / Models / Logic

### Natural Language Processing

**Summarization Algorithm** (`summarized_data.py`):
```
Input: Raw Turkish news article text
1. Text cleaning: Remove excessive whitespace, normalize formatting
2. Sentence splitting: Regex-based sentence boundary detection (split on .!? followed by space)
3. Per-sentence processing:
   a. mT5-based summarization (max_length=60, min_length=15, beam_size=4)
   b. Token cleanup: Remove special model tokens (<extra_id_>, <pad>, </s>)
   c. Quality check: Length validation, special character ratio < 10%
4. Deduplication: Jaccard similarity between summaries (threshold=0.5)
5. Final assembly: Concatenate unique summaries, remove redundant sentences
6. GPT-4o-mini refinement: Fix grammar, improve fluency (temperature=0.2)
Output: Cleaned, concise Turkish summary
```

**Similarity Scoring**: Jaccard Index implementation
```python
similarity = |set(words1) ∩ set(words2)| / |set(words1) ∪ set(words2)|
```

**Quality Control**:
- Minimum sentence length: 20 characters, 3 words
- Maximum special character ratio: 10%
- Duplicate sentence detection threshold: 60% similarity

### Video Processing

**Highlight Selection Algorithm** (`generate_video_shorts.py`):
```
Input: Video file, OpenAI API key
1. Audio Extraction: ffmpeg → 16kHz mono WAV
2. Speech Recognition: faster-whisper (small model) → timestamped segments
3. For each segment (up to max_segments=9):
   a. Send segment + full transcript context to GPT-4
   b. Prompt: Evaluate importance in context (JSON response)
   c. Parse response: {"start": float, "end": float, "important": bool}
   d. If important=true, add to selection
4. Video Composition:
   a. Extract selected time ranges from original video
   b. Generate subtitle images with PIL (outlined text, bottom-aligned)
   c. Composite subtitle overlay on video clips
   d. Concatenate clips with title frame (GPT-4 generated)
5. Export: H.264 video with AAC audio
Output: Short-form highlight video with burned-in subtitles
```

**Subtitle Rendering**: Custom text-to-image with stroke outline
- Font: DejaVu Sans Bold / Liberation Sans Bold (fallback)
- Word wrapping: Width-based with 100px margin
- Text stroke: 4-pixel black outline for readability
- Positioning: Bottom-aligned with configurable margin

### 3D Graphics & Physics

**Camera Movement** (`gallery.html`):
```
Input: Keyboard (WASD) + Mouse movement
1. Velocity calculation: direction_vector * SPEED * delta_time
2. Collision detection: Raycast from camera in movement direction
3. Wall boundaries: Clamp position to gallery limits (±5.5 units)
4. Smooth rotation: Euler angle interpolation for mouse look
Output: Updated camera position and orientation
```

**NPC Behavior System**:
```
State Machine: [Idle] ⟷ [Walking]

Walking State:
1. Pick random target within wall boundaries
2. Calculate direction vector to target
3. Check collision with other NPCs (distance < 0.7 units)
4. If collision-free: Move toward target, rotate to face direction
5. If stuck for >1.5s: Pick new target
6. Apply walk animation: Sinusoidal arm/leg swing
7. If reached target: Transition to Idle

Idle State:
1. Idle timer countdown (3-6 seconds)
2. Breathing animation: Slight body y-position oscillation
3. Arm micro-movements
4. When timer expires: Transition to Walking
```

**Label Billboard Effect**:
```
1. Get NPC head position in world space
2. Project 3D position to 2D screen coordinates
3. Calculate distance from camera
4. If distance > 50 units OR behind camera: Hide label
5. Scale factor = 1.0 / (distance/5 + 0.5)
6. Update label CSS transform with position and scale
```

### Data Scraping & Retry Logic

**Wayback Machine CDX Query**:
```
Parameters: url pattern, date range, category, pagination
1. Query showNumPages to get total page count
2. For each page (limit 10):
   a. Fetch snapshots (limit 100 per page)
   b. For each snapshot URL:
      - If list page: Extract article links → parse each
      - If article page: Parse directly
   c. On failure: Try Availability API fallback
   d. Rate limit: Sleep 2 seconds between requests
3. Aggregate results across categories
Output: JSON array of articles with metadata
```

**HTTP Retry Strategy** (urllib3.Retry):
- Total retries: 3
- Backoff factor: 1 (exponential: 1s, 2s, 4s)
- Status codes: [429, 500, 502, 503, 504]

## Technical Challenges

### 1. Wayback Machine Data Extraction
**Challenge**: Inconsistent HTML structure across archived snapshots spanning 2010-2025. CSS selectors for title, content, date vary by archive date.

**Solution**: Multiple fallback selectors (`select_one` with comma-separated options). Example: `'h1.article-title, h2.news-heading, h3, a[itemprop="url"]'`. Logging warns when elements not found but continues processing.

### 2. Turkish NLP Model Quality
**Challenge**: mT5 model produces token artifacts (`<extra_id_0>`, `<pad>`) and sometimes repetitive or grammatically awkward summaries.

**Solution**: Two-stage pipeline with extensive post-processing:
- Regex cleaning for special tokens
- Sentence-level deduplication (60% similarity threshold)
- GPT-4o-mini as refinement layer with explicit grammar-fix prompt
- Quality gates reject summaries below minimum standards

### 3. API Rate Limiting & Cost Management
**Challenge**: OpenAI and ElevenLabs APIs have rate limits and per-request costs. Real-time summarization/TTS for large datasets would be prohibitively expensive.

**Solution**: 
- Batch preprocessing: Summarization runs offline, results cached in JSON
- TTS on-demand: Only invoked when user clicks "Seslendir" button
- Retry with exponential backoff in scraping layer
- Hardcoded API keys (security risk but acceptable for hackathon/demo)

### 4. 3D Performance with Multiple Objects
**Challenge**: Rendering 100+ crystal panels + multiple animated NPCs can cause frame rate drops on lower-end devices.

**Partial Solution**: 
- Reuse geometries and materials where possible
- Limit NPC count per scene
- Simple collision detection (distance checks, no complex physics)
- No dynamic shadows on NPCs (only static scene shadows)

**Limitation**: No LOD (Level of Detail) system, no frustum culling optimization, all objects render regardless of visibility.

### 5. Cross-Origin Resource Sharing (CORS)
**Challenge**: Browser security prevents frontend from directly calling ElevenLabs API due to CORS policy.

**Solution**: Flask proxy server with Flask-CORS configured for specific origins. Adds latency but enables browser-based TTS.

### 6. Video Processing GPU Dependency
**Challenge**: `faster-whisper` configured with `device="cuda"` in code, fails on CPU-only systems.

**Workaround Required**: Manual code edit to `device="cpu"` or conditional device selection based on CUDA availability check.

### 7. Pointer Lock API User Friction
**Challenge**: Browser security requires user gesture to enable pointer lock (mouse capture for first-person controls). Some users confused by click-to-start interaction.

**Partial Solution**: On-screen instruction in HUD ("Tıklayın ve WASD ile gezinin"). No tutorial or progressive onboarding.

## Performance / Scalability Considerations

### Current Implementation

**Strengths**:
- **Client-side 3D rendering**: Offloads computation to user's GPU, no server rendering bottleneck
- **Static file serving**: index.html and gallery.html can be served from CDN, minimal server infrastructure
- **Lazy TTS**: Audio generated on-demand, not precomputed for all articles
- **JSON-based data**: Fast parsing, no database query overhead

**Performance Bottlenecks**:
- **Single-threaded scraping**: Processes articles sequentially with 2-second delays. ~500 articles × 2s = 16+ minutes
- **No caching layer**: Every TTS request hits ElevenLabs API, even for repeated text
- **Synchronous summarization**: Batch script processes articles one-by-one, no parallelization
- **Frontend data loading**: Loads entire JSON into memory, no pagination or virtual scrolling
- **3D scene complexity**: All news panels created upfront, no dynamic loading/unloading

### Scalability Limitations

**Data Scale**:
- Current: ~500 articles stored in JSON files (hundreds of KB)
- Scaling to 100K+ articles would cause:
  - Frontend JSON parse delays (multi-MB file)
  - Memory pressure in browser
  - Gallery overcrowding (too many panels)

**Concurrent Users**:
- Flask development server (`app.run`) not production-ready
- Single-threaded, no load balancing
- TTS requests queue sequentially
- No rate limiting on API usage (could exceed ElevenLabs quota)

**API Cost Scaling**:
- ElevenLabs: ~$0.18/1000 characters. 10K daily TTS requests × 200 chars = $360/day
- OpenAI GPT-4: ~$0.03/1K tokens for input. Video analysis with long transcripts costly

### Optimizations Implemented

1. **HTTP Connection Pooling**: `requests.Session()` reuses TCP connections in scraping
2. **Retry with Backoff**: Prevents server overload from repeated failed requests
3. **Material Reuse**: three.js materials created once, shared across multiple meshes
4. **Geometry Sharing**: BoxGeometry instances reused for walls/floors
5. **Text Compression**: Summarization reduces content size by ~70% (typical article 500→150 words)

### Missing Optimizations

- No database indexing (date-based queries would be slow at scale)
- No CDN for static assets
- No image optimization/compression (news images served as-is)
- No worker threads for summarization
- No Redis caching for TTS responses
- No WebGL instancing for repeated geometries
- No occlusion culling (renders objects behind walls)

## Limitations & Technical Debt

### Architecture & Code Quality

1. **Hardcoded API Keys** (`summarized_data.py` line 181, `generate_video_shorts.py` line 136): Security vulnerability. Should use environment variables consistently.

2. **No Input Validation**: TTS endpoint accepts arbitrary text length, could cause API errors or excessive costs. Missing regex sanitization for user-provided dates.

3. **Error Handling Gaps**: 
   - Scraping continues silently when content parsing fails
   - Summarization skips failed articles without user notification
   - TTS errors return 400 but don't log details
   - No graceful degradation when APIs unavailable

4. **Mixed Configuration Management**: Some scripts use `.env` (voice.py), others have hardcoded keys. Inconsistent approach.

5. **No Logging Framework**: Uses `print()` and basic `logging` inconsistently. No centralized log aggregation or monitoring.

6. **File Path Assumptions**: Scripts assume data files exist in specific relative paths. No path validation or configuration file.

### Data Management

7. **No Data Versioning**: Overwriting `summarized_data.json` loses previous summaries. No changelog or rollback capability.

8. **CSV for Structured Data** (`aa_haberler.csv`): Poor choice for nested data. Inconsistent with JSON used elsewhere.

9. **No Data Deduplication**: Wayback scraper may collect same article multiple times if archived repeatedly.

10. **Missing Metadata**: No processing timestamp, no data source tracking, no quality scores stored.

### Frontend Issues

11. **No Mobile Support**: First-person WASD controls impossible on touch devices. No alternative control scheme.

12. **Accessibility Violations**: 
    - No keyboard navigation for modals
    - Missing ARIA labels
    - No screen reader support for 3D scene
    - Poor color contrast in some UI elements

13. **Browser Compatibility**: 
    - Pointer Lock API not supported in all browsers
    - WebGL 1.0 used (WebGL 2.0 would be better)
    - No feature detection or fallback for unsupported browsers

14. **No Loading States**: Gallery shows blank screen while fetching JSON. No progress indicator.

15. **Memory Leaks**: three.js objects not properly disposed when changing dates. Repeated navigation could exhaust memory.

### Backend Services

16. **Development Server in Production**: `voice.py` uses `app.run(debug=True)` which is not production-safe.

17. **No Rate Limiting**: TTS endpoint vulnerable to abuse. No request throttling or API key authentication.

18. **CORS Whitelist Incomplete**: Only allows two specific origins. Would need updating for deployment.

19. **No Health Checks**: No `/health` endpoint to monitor service status.

### Video Processing

20. **GPU Hardcoded**: `faster-whisper` always tries CUDA, fails on CPU-only systems without fallback.

21. **No Video Validation**: Accepts any file path, no format/codec checking, unclear error messages.

22. **Temporary File Cleanup**: `temp_audio.wav` not explicitly deleted, could accumulate.

23. **Max Segments Arbitrary**: `max_segments=9` has no justification. Not configurable per video.

### Testing & Documentation

24. **Zero Automated Tests**: No unit tests, integration tests, or end-to-end tests.

25. **No API Documentation**: TTS endpoint lacks OpenAPI/Swagger spec.

26. **Inline Comments Sparse**: Complex algorithms (NPC behavior, similarity scoring) lack explanatory comments.

27. **Requirements.txt Missing**: Dependency installation relies on manual pip install command in README.

### Data Quality

28. **Summarization Quality Inconsistent**: Some summaries still contain duplicates or grammatical errors despite filtering.

29. **News Coverage Gaps**: Wayback scraping only retrieves available archives. Many dates have zero articles.

30. **Category Misclassification**: RSS scraper trusts feed categories, but scraped articles guess from URL path.

## Possible Improvements

### High Priority (Critical for Production)

1. **Environment Variable Management**: 
   - Consolidate all API keys to `.env` file
   - Use `python-dotenv` in all scripts
   - Add `.env.example` template to repository
   - Document required variables in README

2. **Database Migration**:
   - Replace JSON files with PostgreSQL or MongoDB
   - Index by date, category for fast queries
   - Enable pagination for frontend (load 50 articles at a time)
   - Store processing metadata (timestamp, quality scores)

3. **Production-Ready Flask Deployment**:
   - Switch to Gunicorn or uWSGI
   - Add rate limiting (Flask-Limiter)
   - Implement request authentication (API keys or JWT)
   - Configure CORS dynamically from environment variable
   - Add health check endpoint: `GET /health → 200 OK`

4. **Requirements File**:
   ```bash
   pip freeze > requirements.txt
   ```
   Include versions for reproducible builds

5. **Error Handling & Validation**:
   - Add schema validation for TTS requests (max length 5000 chars)
   - Wrap API calls in try-except with specific error messages
   - Return structured error responses: `{"error": "...", "code": 400}`
   - Log errors to file with timestamps

### Medium Priority (Enhances UX/Performance)

6. **TTS Caching Layer**:
   - Use Redis to cache ElevenLabs responses by text hash
   - Reduce API costs by 80%+ for repeated articles
   - Set TTL of 7 days for cache entries
   ```python
   cache_key = hashlib.sha256(text.encode()).hexdigest()
   if redis.exists(cache_key):
       return redis.get(cache_key)
   ```

7. **Asynchronous Scraping**:
   - Use `asyncio` + `aiohttp` for concurrent requests
   - Process 10 articles simultaneously
   - Reduce total scraping time by ~80%
   ```python
   async with aiohttp.ClientSession() as session:
       tasks = [fetch_article(session, url) for url in urls]
       results = await asyncio.gather(*tasks)
   ```

8. **Frontend Performance**:
   - Implement frustum culling (only render visible panels)
   - Use three.js InstancedMesh for repeated geometries (walls, NPCs)
   - Lazy load images (load on modal open, not upfront)
   - Paginate data fetching (fetch date range, not all articles)
   - Add loading spinner during JSON fetch

9. **Mobile Controls**:
   - Add virtual joystick for touch devices
   - Implement gyroscope camera control option
   - Pinch-to-zoom for modal images
   - Responsive layout adjustments for small screens

10. **Video Processing Robustness**:
    - Detect CUDA availability: `torch.cuda.is_available()`
    - Fallback to CPU if GPU unavailable
    - Validate video format before processing (ffprobe)
    - Clean up temporary files in `finally` block
    - Make `max_segments` configurable via command-line argument

### Low Priority (Nice to Have)

11. **Progressive Web App (PWA)**:
    - Add service worker for offline caching
    - Enable "Add to Home Screen" on mobile
    - Cache 3D assets and recently viewed news

12. **Analytics Integration**:
    - Track most viewed news categories
    - Measure average session duration in gallery
    - Monitor TTS usage patterns
    - Log NPC interaction rates

13. **Advanced NLP Features**:
    - Named entity recognition (extract people, places)
    - Sentiment analysis (tag news as positive/negative/neutral)
    - Topic clustering (group related articles)
    - Multi-language support (translate summaries)

14. **Enhanced 3D Experience**:
    - Particle effects for category transitions
    - Ambient background music (era-appropriate)
    - VR headset support (WebXR API)
    - Minimap for navigation
    - Teleport system for large galleries

15. **Social Features**:
    - Share specific news articles (URL with article ID)
    - Collaborative gallery tours (WebRTC multiplayer)
    - Comment system for articles
    - User bookmarking/favorites

16. **Admin Dashboard**:
    - Web UI to trigger scraping/summarization jobs
    - View processing status and error logs
    - Manually approve/reject summaries
    - Configure category mappings

17. **Automated Testing**:
    - Unit tests for NLP functions (pytest)
    - Mock API responses for reproducible tests
    - Visual regression tests for 3D scenes (Percy, Applitools)
    - Load testing for TTS endpoint (Locust)

18. **CI/CD Pipeline**:
    - GitHub Actions workflow:
      1. Lint Python (flake8) and JavaScript (ESLint)
      2. Run unit tests
      3. Build Docker image
      4. Deploy to staging environment
    - Automatic dependency updates (Dependabot)

19. **Content Moderation**:
    - Filter inappropriate content from scraped news
    - Flag potentially sensitive topics
    - Age-appropriate content warnings

20. **Data Visualization Enhancements**:
    - Timeline view (linear scrubber across dates)
    - Heatmap of news density by date/category
    - Network graph of related articles
    - Word cloud for trending topics

---

**Document Version**: 1.0  
**Last Updated**: 2026-02-03  
**Lines of Code**: ~3,533 (Python backend + HTML/CSS/JS frontend)  
**Primary Language**: JavaScript (frontend), Python (backend)
