/**
 * Elevate Scoring Adapter
 * Premium experience and high-value event scoring for exclusive events
 */

const elevateAdapter = {
  name: 'Elevate',
  brand: 'businesscalendar',
  
  async computeScore(entityData, options = {}) {
    const { entityType, entity } = entityData;
    
    if (entityType !== 'event') {
      throw new Error('Elevate only supports event scoring');
    }

    const scores = await this.calculateElevateScores(entity);
    
    return {
      overallScore: scores.overallScore,
      dimensions: {
        exclusivity: scores.exclusivity,
        premiumValue: scores.premiumValue,
        experienceQuality: scores.experienceQuality
      },
      reasoning: scores.reasoning,
      status: 'completed'
    };
  },

  async calculateElevateScores(event) {
    const title = event.title?.toLowerCase() || '';
    const description = event.description?.toLowerCase() || '';
    const category = event.category?.toLowerCase() || '';
    
    // Exclusivity (1-10 scale)
    let exclusivity = 3; // baseline
    
    const exclusiveKeywords = [
      'exclusive', 'vip', 'premium', 'private', 'invitation-only',
      'limited', 'select', 'elite', 'executive', 'luxury'
    ];
    
    exclusiveKeywords.forEach(keyword => {
      if (title.includes(keyword) || description.includes(keyword)) {
        exclusivity += 2;
      }
    });
    
    if (category === 'executive' || category === 'premium') {
      exclusivity += 2;
    }
    
    exclusivity = Math.min(exclusivity, 10);
    
    // Premium Value (1-10 scale)
    let premiumValue = 4; // baseline
    
    const premiumKeywords = [
      'high-end', 'luxury', 'premium', 'first-class', 'deluxe',
      'upscale', 'sophisticated', 'refined', 'exceptional', 'world-class'
    ];
    
    premiumKeywords.forEach(keyword => {
      if (title.includes(keyword) || description.includes(keyword)) {
        premiumValue += 1.5;
      }
    });
    
    premiumValue = Math.min(premiumValue, 10);
    
    // Experience Quality (1-10 scale)
    let experienceQuality = 5; // baseline
    
    const qualityKeywords = [
      'experience', 'curated', 'bespoke', 'tailored', 'personalized',
      'immersive', 'exceptional', 'memorable', 'extraordinary', 'unique'
    ];
    
    qualityKeywords.forEach(keyword => {
      if (title.includes(keyword) || description.includes(keyword)) {
        experienceQuality += 1;
      }
    });
    
    experienceQuality = Math.min(experienceQuality, 10);
    
    // Overall score (weighted average: exclusivity 35%, premium 35%, experience 30%)
    const overallScore = Math.round(
      exclusivity * 0.35 + 
      premiumValue * 0.35 + 
      experienceQuality * 0.30
    );
    
    const reasoning = `Elevated experience featuring ${exclusivity >= 7 ? 'high exclusivity' : 'selective access'} with ${premiumValue >= 7 ? 'premium value' : 'quality offerings'} and exceptional experience design.`;
    
    return {
      overallScore,
      exclusivity,
      premiumValue,
      experienceQuality,
      reasoning: reasoning.slice(0, 240)
    };
  }
};

module.exports = { elevateAdapter };