import React from "react"
import { Row, Col, Container } from "react-bootstrap"
import "./../styles/components/pageHeading.scss"

const PageHeading = ({ pageTitle, styleFilled }) => {
  return (
    <Container fluid className="heading">
      <div className="keyvisual">
        <Container className="item">
          <Row>
            <Col>
              <h1>{pageTitle}</h1>
            </Col>
          </Row>
        </Container>
        {styleFilled ? (
          <div className={"success-line-filled " + styleFilled}></div>
        ) : (
          <div className="success-line"></div>
        )}
      </div>
    </Container>
  )
}

export default PageHeading
