import React from "react"
import { Row, Col, Container } from "react-bootstrap"
import { StaticQuery, graphql } from "gatsby"
import ClassificationRow from "./classificationCard"

const BoxDetailedMethods = ({ small, orderedMethods }) => {
  return (
    <StaticQuery
      query={graphql`
        query DetailedMethodQuery {
            allSitePage(filter: {context: {method: {id: {regex: "/.*\\S.*/"}}}}) {
              nodes {
                  context {
                  method {
                      name
                      id
                      abbr
                      classification
                      question
                  }
                  }
                  path
              }
            }
        }
      `}
      render={data => {
        var orderedIdx = []
        // if order is given, reorder methods. Else take all and print in default order
        if (orderedMethods && orderedMethods.length > 0) {
          orderedMethods.forEach(m => {
            orderedIdx.push(
              data.allSitePage.nodes
                .map(e => {
                  return e.context.method.id
                })
                .indexOf(m)
            )
          })
        } else {
          for (var i = 0; i < data.allSitePage.nodes.length; i++) {
            orderedIdx.push(i)
          }
        }

        return (
          <Container className="gradientYellowGreen methodDetailedBoxes">
            <Row className="methodDetailedBoxes content-area">
              <Col className="big-list">
                <ol>
                  {orderedIdx.map((key, idx) => {
                    var method = data.allSitePage.nodes[key].context.method
                    var methodName =
                      method.abbr.toLowerCase() !== method.name.toLowerCase()
                        ? `${method.abbr} (${method.name})`
                        : `${method.name}`

                    return (
                      <li key={idx}>
                        <div
                          className={"methodBlock " + (small ? "small" : "")}
                          key={`methodBlock-${idx}`}
                        >
                          <a href={data.allSitePage.nodes[key].path}>
                            <h3>{methodName}</h3>
                            <ClassificationRow
                              itemList={method.classification}
                            />
                            <div
                              className="text"
                              dangerouslySetInnerHTML={{
                                __html: method.question,
                              }}
                            />
                          </a>
                        </div>
                      </li>
                    )
                  })}
                </ol>
              </Col>
            </Row>
          </Container>
        )
      }}
    />
  )
}

/*

return (
                     
                    )
        {
          "context": {
            "method": {
              "name": "Partial Dependence Plots (PDP) & Individual Conditional Expectation (ICE)",
              "id": "pdp_ice",
              "classification": [
                "scopeBoth",
                "featureRelevance",
                "perturbation",
                "visual"
              ],
              "question": "PDP: Wie ist der durchschnittliche Zusammenhang zwischen dem betrachteten (von den anderen unabhängigen) Feature und der Vorhersage? <br> ICE: Wie ist der dateninstanzspezifische Zusammenhang zwischen dem betrachteten (von den anderen unabhängigen) Feature und der Vorhersage?"
            }
          },
          "path": "/method/pdp_ice/"
        },
        --> filter if context.method = null !!!
*/

export default BoxDetailedMethods
