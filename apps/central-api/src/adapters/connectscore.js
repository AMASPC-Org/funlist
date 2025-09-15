/**
 * ConnectScore Scoring Adapter
 * Business networking and professional connection scoring for BusinessCalendar
 */

const connectScoreAdapter = {
  name: 'ConnectScore',
  brand: 'businesscalendar',
  
  async computeScore(entityData, options = {}) {
    const { entityType, entity } = entityData;
    
    if (entityType !== 'event') {
      throw new Error('ConnectScore only supports event scoring');
    }

    const scores = await this.calculateConnectScores(entity);
    
    return {
      overallScore: scores.overallScore,
      dimensions: {
        networkingPotential: scores.networkingPotential,
        businessValue: scores.businessValue,
        professionalGrowth: scores.professionalGrowth
      },
      reasoning: scores.reasoning,
      status: 'completed'
    };
  },

  async calculateConnectScores(event) {
    const title = event.title?.toLowerCase() || '';
    const description = event.description?.toLowerCase() || '';
    const category = event.category?.toLowerCase() || '';
    
    // Networking Potential (1-10 scale)
    let networkingPotential = 4; // baseline
    
    const networkingKeywords = [
      'networking', 'conference', 'meetup', 'summit', 'workshop',
      'seminar', 'panel', 'discussion', 'connect', 'collaboration'
    ];
    
    networkingKeywords.forEach(keyword => {
      if (title.includes(keyword) || description.includes(keyword)) {
        networkingPotential += 1;
      }
    });
    
    if (category === 'business' || category === 'professional') {
      networkingPotential += 1;
    }
    
    networkingPotential = Math.min(networkingPotential, 10);
    
    // Business Value (1-10 scale)
    let businessValue = 4; // baseline
    
    const businessKeywords = [
      'business', 'entrepreneur', 'startup', 'investment', 'strategy',
      'marketing', 'sales', 'leadership', 'growth', 'innovation'
    ];
    
    businessKeywords.forEach(keyword => {
      if (title.includes(keyword) || description.includes(keyword)) {
        businessValue += 1;
      }
    });
    
    businessValue = Math.min(businessValue, 10);
    
    // Professional Growth (1-10 scale)
    let professionalGrowth = 5; // baseline
    
    const growthKeywords = [
      'career', 'skills', 'training', 'certification', 'learning',
      'development', 'mentorship', 'coaching', 'education', 'workshop'
    ];
    
    growthKeywords.forEach(keyword => {
      if (title.includes(keyword) || description.includes(keyword)) {
        professionalGrowth += 1;
      }
    });
    
    professionalGrowth = Math.min(professionalGrowth, 10);
    
    // Overall score (weighted average: networking 40%, business 35%, growth 25%)
    const overallScore = Math.round(
      networkingPotential * 0.4 + 
      businessValue * 0.35 + 
      professionalGrowth * 0.25
    );
    
    const reasoning = `Strong professional value with ${networkingPotential >= 7 ? 'excellent networking opportunities' : 'good connections'} and ${businessValue >= 7 ? 'high business impact' : 'solid business relevance'}.`;
    
    return {
      overallScore,
      networkingPotential,
      businessValue,
      professionalGrowth,
      reasoning: reasoning.slice(0, 240)
    };
  }
};

module.exports = { connectScoreAdapter };