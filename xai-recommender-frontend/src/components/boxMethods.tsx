import React from "react"
import { BsBook } from "react-icons/bs"
import { Row, Col, Container } from "react-bootstrap"
import { StaticQuery, graphql } from "gatsby"

const BoxMethods = ({ excludeMethods, currentMethod }) => {
  return (
    <StaticQuery
      query={graphql`
      query MethodQuery {
        allSitePage(filter: {context: {method: {id: {regex: "/.*\\S.*/"}}}}) {
          nodes {
              context {
                method {
                  name
                  id
                }
              }
              path
            }
          }
        }
      `}
      render={data => (
        <Container>
          <Row className="methodBoxes">
            {Object.keys(data.allSitePage.nodes).map((key, idx) => {
              return excludeMethods &&
                excludeMethods.includes(
                  data.allSitePage.nodes[key].context.method.id
                ) ? null : (
                <div className="methodBlock" key={`methodBlock-${idx}`}>
                  <a href={data.allSitePage.nodes[key].path}>
                    <button
                      className={
                        "btn btn-primary " +
                        (currentMethod &&
                        currentMethod ==
                          data.allSitePage.nodes[key].context.method.id
                          ? "suggested"
                          : "")
                      }
                    >
                      {data.allSitePage.nodes[key].context.method.name}
                    </button>
                  </a>
                </div>
              )
            })}
          </Row>
        </Container>
      )}
    />
  )
}

/*
        {
          "context": {
            "method": {
              "name": "Partial Dependence Plots (PDP) & Individual Conditional Expectation (ICE)",
              "abbr": "PDP + ICE"
            }
          },
          "path": "/method/pdp_ice/"
        },
        --> filter if context.method = null !!!
*/

export default BoxMethods
