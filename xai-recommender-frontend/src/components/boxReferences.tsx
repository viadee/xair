import React from "react"
import { BsBook } from "react-icons/bs"
import { Row, Col, Container } from "react-bootstrap"

const BoxReferences = ({ references }) => {
  if (references && Object.keys(references).length > 0) {
    return (
      <Container fluid className="references">
        <Container>
          <Row>
            <Col md="1">
              <span>
                <BsBook />
              </span>
            </Col>
            <Col md="11">
              <h2>Referenzen</h2>
              <ol>
                {Object.keys(references).map((key, idx) => {
                  return (
                    <li key={`ref${key}`}>
                      <a id={`ref${key}`} />
                      <div
                        id={`ref-${key}`}
                        dangerouslySetInnerHTML={{ __html: references[key] }}
                      />
                    </li>
                  )
                })}
              </ol>
            </Col>
          </Row>
        </Container>
      </Container>
    )
  } else {
    return null
  }
}

export default BoxReferences
