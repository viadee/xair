import React from "react"
import { Link } from "gatsby"
import { BiRightArrow } from "react-icons/bi"

import { Navbar, Nav, Container } from "react-bootstrap"
import RecommendationContext from "./../context/recommendationContext"

const RecommenderNavbar = ({ pageInfo }) => {
  return (
    <RecommendationContext.Consumer>
      {rec => (
        <div>
          {rec.result == null ||
          rec.result.recommendation.length == 0 ? null : (
            <Navbar expand="lg" id="site-navbar">
              <Container>
                <Navbar.Toggle aria-controls="basic-navbar-nav" />
                <Navbar.Collapse id="basic-navbar-nav">
                  <Nav
                    className="mr-auto"
                    activeKey={pageInfo && pageInfo.pageName}
                  >
                    <Link to="/start" className="link-no-style">
                      <Nav.Link as="span" eventKey="start">
                        Inputs
                      </Nav.Link>
                    </Link>

                    <BiRightArrow />

                    <Link to="/result" className="link-no-style">
                      <Nav.Link as="span" eventKey="result">
                        Recommendation
                      </Nav.Link>
                    </Link>
                    <BiRightArrow />

                    <Link to="/why" className="link-no-style">
                      <Nav.Link as="span" eventKey="why">
                        Why?
                      </Nav.Link>
                    </Link>
                    <BiRightArrow />
                    <Link
                      to={"/method/" + rec.result.recommendation[0]["name"]}
                      className="link-no-style"
                    >
                      <Nav.Link as="span" eventKey="method">
                        Suggested method '
                        {rec.result.recommendation[0]["label"]}'
                      </Nav.Link>
                    </Link>
                    <BiRightArrow />

                    <Link
                      to={
                        "/implementation/" +
                        rec.result.recommendation[0]["name"]
                      }
                      className="link-no-style"
                    >
                      <Nav.Link as="span" eventKey="implementation">
                        Suggested implementation '
                        {rec.result.recommendation[0]["label"]}'
                      </Nav.Link>
                    </Link>
                    <BiRightArrow />

                    <Link to="/further_steps" className="link-no-style">
                      <Nav.Link as="span" eventKey="further_steps">
                        Further steps
                      </Nav.Link>
                    </Link>
                  </Nav>
                </Navbar.Collapse>
              </Container>
              {/* <Container> */}
            </Navbar>
          )}
        </div>
      )}
    </RecommendationContext.Consumer>
  )
}

export default RecommenderNavbar
