module.exports = {
  pathPrefix: "/xai-xps-webapp",
  siteMetadata: {
    title: `XAI Recommender`,
    description: `This XAI recommendation system provides recommendations on the application of appropriate XAI methods for ML models, taking into account the data, model, and usage context. This guarantees that plausible explanations are obtained.`,
    keywords: ["XAI", "Explainable AI", "Recommendation", "Expert System", "XAI XPS"],
    author: `Verena Barth`,
  },
  plugins: [
    `gatsby-plugin-react-helmet`,
    `gatsby-plugin-typescript`,
    `gatsby-plugin-sass`,
    /*
    {
      resolve: `gatsby-plugin-manifest`,
      options: {
        name: `gatsby-plugin-manifest`,
        icon: `static/images/favicon.png`
      }
    }
    */
  ],
}
