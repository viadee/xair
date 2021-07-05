import React from "react"
import Layout from "./../components/layout"
import { Row, Col, Container } from "react-bootstrap"
import PageHeading from "./../components/pageHeading"
import { BsCodeSlash } from "react-icons/bs"
import { BsExclamationCircle } from "react-icons/bs"
import { BiRightArrow } from "react-icons/bi"
import { AiOutlineTool } from "react-icons/ai"
import BoxReferences from "./../components/boxReferences"
import "./../styles/pages/methods.scss"

const Implementation = ({ pageContext }) => {
  const { abbr, implementation } = pageContext.implementation
  const prereqs = implementation.prereqs

  return (
    <Layout pageInfo={{ pageName: `Implementation for '${abbr}'` }}>
      <PageHeading
        pageTitle={`Implementation for '${abbr}'`}
        styleFilled={"gray"}
      />
      <Container fluid className="keyvisual gray" style={{ minHeight: "30vh" }}>
        <Container className="align-items-center">
          <Row>
            <Col>
              <h2>Welche Implementierung wird empfohlen?</h2>
              <div
                className="text"
                dangerouslySetInnerHTML={{
                  __html: implementation.recommendation,
                }}
              />
            </Col>
          </Row>
        </Container>
        <div className="success-line" />
      </Container>
      <Container fluid style={{ marginTop: "-2.5rem" }}>
        <PageHeading
          pageTitle={`${abbr} Implementierung: ${implementation.name}`}
        />
      </Container>

      <Container className="page implementation">
        <Row>
          <Col md="1"></Col>
          <Col>
            <div className="linkBox">
              <div>
                <BiRightArrow />
                <a href={`${implementation.doc_link}`}>Dokumentation</a>
              </div>
              <div>
                <BiRightArrow />
                <a href={`${implementation.code_link}`}>Sourcecode</a>
              </div>
            </div>
          </Col>
        </Row>
        <Row className="section split">
          <Col md="1"></Col>
          <Col md="6" sm="12" className="prereqList text">
            <h2>Was benötigt man dafür?</h2>
            <ul>
              <li>
                {prereqs.model
                  ? "Zugriff auf Modell"
                  : "Zugriff auf Vorersagefunktion"}
              </li>
              <li>
                <b>Trainingsdaten</b>
                <ul>
                  {prereqs.data.info ? <li>{prereqs.data.info}</li> : null}
                  <li>Kategorische Features: {prereqs.data.categorical}</li>
                  <li>Numerische Features: {prereqs.data.numerical}</li>
                  <li>Zugriff auf Spaltennamen: {prereqs.data.colNames}</li>
                </ul>
              </li>
              {prereqs.trueLabel ? <li>Label (True Outcome)</li> : null}
              {prereqs.additional &&
                prereqs.additional.map(info => <li>{info}</li>)}
            </ul>
          </Col>
          <Col md="5" sm="12">
            <h2>Was ist das Ergebnis?</h2>
            <div
              className="text"
              dangerouslySetInnerHTML={{
                __html: implementation.result,
              }}
            />
          </Col>
        </Row>
        <Row className="section green">
          <Col md="1">
            <BsExclamationCircle />
          </Col>
          <Col md="11">
            <h1>Was muss man beachten?</h1>
          </Col>
        </Row>
        {implementation.hintsUsage ? (
          <Row className="section">
            <Col md="1">
              <span>
                <AiOutlineTool />
              </span>
            </Col>
            <Col md="11">
              <h2>Hinweise zur Anwendung der Methode</h2>
              <ul>
                {implementation.hintsUsage.map(hint => (
                  <li>
                    <div
                      className="text"
                      dangerouslySetInnerHTML={{
                        __html: hint,
                      }}
                    />
                  </li>
                ))}
              </ul>
            </Col>
          </Row>
        ) : null}
        {Object.keys(implementation.hintsImpl).length > 0 ? (
          <Row className="section">
            <Col md="1">
              <span>
                <BsCodeSlash />
              </span>
            </Col>
            <Col md="11">
              <h2>Hinweise zur Parameterauswahl für die Implementierung</h2>
              <ul>
                {Object.keys(implementation.hintsImpl).map((key, idx) => {
                  return (
                    <li key={`param-${idx}`}>
                      <span className="param">{key}</span>
                      <br />
                      <div
                        className="text paramText"
                        dangerouslySetInnerHTML={{
                          __html: implementation.hintsImpl[key],
                        }}
                      />
                    </li>
                  )
                })}
              </ul>
            </Col>
          </Row>
        ) : null}
      </Container>
      <BoxReferences references={implementation.references} />
    </Layout>
  )
}

export default Implementation

/*



*/
