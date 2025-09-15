/**
 * Funalytics Scoring Adapter
 * Implements the original FunList.ai scoring algorithm
 */

const funalyticsAdapter = {
  name: 'Funalytics',
  brand: 'funlist',
  
  async computeScore(entityData, options = {}) {
    const { entityType, entity } = entityData;
    
    if (entityType !== 'event') {
      throw new Error('Funalytics only supports event scoring');
    }

    // Use existing Funalytics scoring logic
    const scores = await this.calculateFunalyticsScores(entity);
    
    return {
      overallScore: scores.overallScore,
      dimensions: {
        communityVibe: scores.communityVibe,
        familyFun: scores.familyFun
      },
      reasoning: scores.reasoning || 'AI-powered fun analysis based on event characteristics.',
      status: 'completed'
    };
  },

  async calculateFunalyticsScores(event) {
    // Reuse existing Funalytics calculation logic
    const title = event.title?.toLowerCase() || '';
    const description = event.description?.toLowerCase() || '';
    const category = event.category?.toLowerCase() || '';
    
    // Community Vibe calculation (1-10 scale)
    let communityVibe = 5; // baseline
    
    const communityKeywords = [
      'community', 'local', 'neighborhood', 'downtown', 'festival',
      'market', 'fair', 'block party', 'gathering', 'social'
    ];
    
    communityKeywords.forEach(keyword => {
      if (title.includes(keyword) || description.includes(keyword)) {
        communityVibe += 1;
      }
    });
    
    if (category === 'community' || category === 'festival') {
      communityVibe += 1;
    }
    
    communityVibe = Math.min(communityVibe, 10);
    
    // Family Fun calculation (1-10 scale)
    let familyFun = 5; // baseline
    
    const familyKeywords = [
      'family', 'kids', 'children', 'playground', 'park',
      'educational', 'workshop', 'crafts', 'games', 'fun'
    ];
    
    familyKeywords.forEach(keyword => {
      if (title.includes(keyword) || description.includes(keyword)) {
        familyFun += 1;
      }
    });
    
    if (category === 'family' || category === 'education') {
      familyFun += 1;
    }
    
    familyFun = Math.min(familyFun, 10);
    
    // Overall score (weighted average)
    const overallScore = Math.round((communityVibe * 0.6 + familyFun * 0.4));
    
    const reasoning = `High fun score because of ${communityVibe >= 7 ? 'strong community focus' : 'local engagement'}${familyFun >= 7 ? ' and family-friendly activities' : ''}.`;
    
    return {
      overallScore,
      communityVibe,
      familyFun,
      reasoning: reasoning.slice(0, 240) // Limit to 240 chars
    };
  }
};

module.exports = { funalyticsAdapter };