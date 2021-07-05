/**
 * Implement Gatsby's Node APIs in this file.
 *
 * See: https://www.gatsbyjs.org/docs/node-apis/
 *
 *
 */

exports.createPages = ({ actions: { createPage } }) => {
  var glob = require("glob")
  var path = require("path")

  glob.sync("./static/methods/**/*.json").forEach(function(file) {
    console.log("Parsing method file: ", file)
    const method = require(path.resolve(file))

    // create method page
    createPage({
      path: `/method/${method.id.toLowerCase()}/`,
      component: require.resolve("./src/templates/method.js"),
      context: { method },
    })
    // create implementation page
    var implementation = {
      name: method.name,
      abbr: method.abbr,
      implementation: method.implementation,
    }
    createPage({
      path: `/implementation/${method.id.toLowerCase()}/`,
      component: require.resolve("./src/templates/implementation.js"),
      context: { implementation },
    })
  })
}
