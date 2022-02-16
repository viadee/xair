/**
 * Layout component that queries for data
 * with Gatsby's StaticQuery component
 *
 * See: https://www.gatsbyjs.org/docs/static-query/
 */

import React from "react"
import { StaticQuery, graphql, Link } from "gatsby"
import SEO from "../components/seo"
import { BiHeart } from "react-icons/bi"

import { Container, Row, Col } from "react-bootstrap"

import Header from "./header"
import RecommenderNavbar from "./navBar"

const Layout = ({ children, pageInfo }) => (
  <StaticQuery
    query={graphql`
      query SiteTitleQuery {
        site {
          siteMetadata {
            title
            keywords
          }
        }
      }
    `}
    render={data => (
      <>
        <SEO title={pageInfo.pageName} />
        <Container fluid className="content">
          <Header siteTitle={data.site.siteMetadata.title} />
          <RecommenderNavbar pageInfo={pageInfo} />
          <Container fluid>
            <main>{children}</main>
          </Container>
        </Container>
        {
          <Container fluid style={{ paddingLeft: 0, paddingRight: 0 }}>
            <Row>
              <Col className="footer-col">
                <footer>
                  <span>
                    © {new Date().getFullYear()}, {" "}
                    <a href="https://www.viadee.de/">
                      viadee Unternehmensberatung AG
                    </a>
                  </span>
                  <Link to="/feedback" className="link-no-style">
                    Give feedback <BiHeart />
                  </Link>
                  <Link to="/faq" className="link-no-style">
                    FAQ
                  </Link>
                </footer>
              </Col>
            </Row>
          </Container>
        }
      </>
    )}
  />
)

export default Layout
