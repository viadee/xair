import React from "react"
import { AiOutlineQuestionCircle } from "react-icons/ai"
import { BiDownArrow } from "react-icons/bi"
import {
  Row,
  Col,
  Container,
  OverlayTrigger,
  Tooltip,
  Accordion,
  Card,
  Button,
} from "react-bootstrap"
import Layout from "../components/layout"
import PageHeading from "../components/pageHeading"
import BoxMethods from "../components/boxMethods"

const FAQPage = () => {
  let opened = null
  if (typeof window !== "undefined") {
    opened = window.location.href.split("#")[1]
  }

  return (
    <Layout pageInfo={{ pageName: "FAQ" }}>
      <PageHeading pageTitle="FAQ" />
      <Container>
        <Accordion defaultActiveKey={opened ? opened : "whyUseSystem"}>
          <Card>
            <Card.Header>
              <Accordion.Toggle
                as={Card.Header}
                variant="link"
                eventKey="whyxai"
              >
                <Row className="section">
                  <Col md="1">
                    <span>
                      <AiOutlineQuestionCircle />
                    </span>
                  </Col>
                  <Col md="10">
                    <h3>Why should I use Explainable AI (XAI)?</h3>
                  </Col>
                  <Col md="1">
                    <span>
                      <BiDownArrow />
                    </span>
                  </Col>
                </Row>
              </Accordion.Toggle>
            </Card.Header>
            <Accordion.Collapse eventKey="whyxai">
              <Card.Body>
                <a id="whyxai" />
                <div className="answer">
                  <p>
                    Machine Learning (ML), as an area of Artificial Intelligence
                    (AI) that uses various mathematical methods to extract
                    knowledge autonomously from a large amount of data, is
                    becoming increasingly important. Unfortunately, the
                    resulting ML models and their decision-making processes are
                    usually incomprehensible to humans due to their complexity.
                    This paucity of transparency of these so-called black-boxes
                    is a major drawback and an obstacle to their use. Especially
                    in critical areas such as autonomous driving, law
                    enforcement, military or medicine, an explanation or
                    justification of the behaviors and decisions is essential
                    for the comprehensibility, fairness and safety of a ML
                    application. Indeed, many examples demonstrate the
                    imperfections of these algorithms. These range from gender
                    stereotypes in natural language processing&nbsp;
                    <a href="https://arxiv.org/pdf/1607.06520.pdf">
                      (Bolukbasi et al. 2016)
                    </a>
                    , to discrimination against women in&nbsp;
                    <a href="https://www.reuters.com/article/us-amazon-com-jobs-automation-insight/amazon-scraps-secret-ai-recruiting-tool-that-showed-bias-against-women-idUSKCN1MK08G">
                      &nbsp;Amazon's automated hiring process
                    </a>
                    , to racism in an&nbsp;
                    <a href="https://www.propublica.org/article/machine-bias-risk-assessments-in-criminal-sentencing">
                      &nbsp;algorithm
                    </a>
                    &nbsp;used in the United States that determines criminal
                    sentences by predicting the likelihood of committing a
                    future crime.
                  </p>
                  <p>
                    There are quite a few sites tracking incidents caused by AI:
                    <br />
                  </p>
                  <ul>
                    <li>
                      <a href="https://incidentdatabase.ai/">
                        AIID Incident Database
                      </a>
                    </li>
                    <li>
                      <a href="https://github.com/jphall663/awesome-machine-learning-interpretability/blob/master/README.md#ai-incident-tracker">
                        AI Incident Tracker
                      </a>
                    </li>
                  </ul>
                  <p>
                    {" "}
                    Governments are also endorsing to the need for transparency
                    of these systems: In May 2018, the pan-European General Data
                    Protection Regulation (GDPR) came into force, which requires
                    that for automated decision-making, data subjects be
                    provided with "meaningful information about the logic
                    involved and the scope and intended effects of such
                    processing"{" "}
                    <a href="https://eur-lex.europa.eu/legal-content/EN/TXT/PDF/?uri=CELEX:32016R0679&from=EN">
                      (Art. 13(2)(f) , Art. 14(2)(g))
                    </a>
                    . The actual usage of XAI methods is therefore very
                    important to ensure or improve the quality of the model, to
                    make it more robust and traceable, and ultimately to build
                    user trust through fairness and transparency. <br />
                    <br />
                  </p>

                  <h5>
                    Great resources related to XAI (articles, papers, news):
                  </h5>
                  <ul>
                    <li>
                      <a href="https://christophm.github.io/interpretable-ml-book">
                        Book: Interpretable Machine Learning
                      </a>
                    </li>
                    <li>
                      <a href="https://fairmlbook.org">
                        Book: Fairness and machine learning
                      </a>
                    </li>

                    <li>
                      <a href="https://github.com/jphall663/awesome-machine-learning-interpretability">
                        GitHub: Awesome machine learning interpretability
                      </a>
                    </li>
                    <li>
                      <a href="https://github.com/anguyen8/XAI-papers">
                        GitHub: Papers on Explainable Artificial Intelligence
                      </a>
                    </li>
                    <li>
                      <a href="https://github.com/jphall663/hc_ml ">
                        GitHub: Toward Responsible Machine Learning
                      </a>
                    </li>
                    <li>
                      <a href="https://github.com/pbiecek/xai_resources">
                        GitHub: Interesting resources related to XAI
                      </a>
                    </li>
                  </ul>
                </div>
              </Card.Body>
            </Accordion.Collapse>
          </Card>

          <Card>
            <Card.Header>
              <Accordion.Toggle
                as={Card.Header}
                variant="link"
                eventKey="whyUseSystem"
              >
                <Row className="section">
                  <Col md="1">
                    <span>
                      <AiOutlineQuestionCircle />
                    </span>
                  </Col>
                  <Col md="10">
                    <h3>Why should I use this XAI Recommender?</h3>
                  </Col>
                  <Col md="1">
                    <span>
                      <BiDownArrow />
                    </span>
                  </Col>
                </Row>
              </Accordion.Toggle>
            </Card.Header>
            <Accordion.Collapse eventKey="whyUseSystem">
              <Card.Body>
                <a id="whyUseSystem" />
                <div className="answer">
                  <p>
                    Recent XAI research has presented a variety of XAI methods
                    and implementations in the form of stand-alone prototype
                    solutions. However, these are hardly used in practice. This
                    is partly because XAI is a new and rapidly developing field,
                    and partly because the existing knowledge is scattered and
                    needs to be organized.
                  </p>
                  <p>
                    Some scientific publications classify diverse methods
                    hierarchically, but rarely provide concrete guidelines or
                    advices for their application. Government agencies such as
                    the Federal Office for Information Security (BSI) point out
                    the relevance of explainability of AI systems and that
                    method-specific properties of inputs must be considered in
                    the selection process, and plausible explanations must be
                    enabled{" "}
                    <a href="https://www.bsi.bund.de/SharedDocs/Downloads/EN/BSI/CloudComputing/AIC4/AI-Cloud-Service-Compliance-Criteria-Catalogue_AIC4.pdf;jsessionid=0E1AECBC4DB1B1AD0926B3799C724231.internet482?__blob=publicationFile&v=4">
                      (Federal Office for Information Security 2021, p. 41)
                    </a>
                    . However, it does not provide information to help users
                    successfully select and apply an XAI method that is
                    appropriate in this sense.
                  </p>
                  <p>
                    So, not all XAI methods are ideally suited in all contexts
                    of use. For example, results of perturbation-based methods
                    can be falsely influenced by correlations in the input
                    features.
                  </p>
                  <p>
                    The <b>XAI Recommender</b> considers all
                    suitability-influencing parameters and suggests a suitable
                    method for your data and model context. For the application,
                    only vague knowledge about the training dataset and the
                    context of use is assumed.
                  </p>
                  <p>
                    In addition to a justified method suggestion, it also
                    provides an explanation of the method, a recommended
                    implementation and hints for the application. Thus, you not
                    only get support for the (quick) selection, but also for the
                    application! Furthermore, information about all methods in
                    this system will be provided.
                    <br />
                    <br />
                  </p>
                  <h5>Short summary of benefits using the XAI Recommender</h5>
                  <ul>
                    <li>
                      Get a justified recommendation of an applicable XAI method
                    </li>
                    <li>
                      Learn which XAI method should be used under which
                      circumstances
                    </li>
                    <li>
                      Get a suggested implementation with some hints for it’s
                      application
                    </li>
                    <li>Inform yourself about all available XAI methods</li>
                    <li>
                      Learn German (sorry, information pages are currently not
                      available in English){" "}
                    </li>
                  </ul>
                </div>
              </Card.Body>
            </Accordion.Collapse>
          </Card>

          <Card>
            <Card.Header>
              <Accordion.Toggle
                as={Card.Header}
                variant="link"
                eventKey="whatsSuitability"
              >
                <Row className="section">
                  <Col md="1">
                    <span>
                      <AiOutlineQuestionCircle />
                    </span>
                  </Col>
                  <Col md="10">
                    <h3>WHAT DOES IT MEAN IF A XAI METHOD IS SUITABLE?</h3>
                  </Col>
                  <Col md="1">
                    <span>
                      <BiDownArrow />
                    </span>
                  </Col>
                </Row>
              </Accordion.Toggle>
            </Card.Header>
            <Accordion.Collapse eventKey="whatsSuitability">
              <Card.Body>
                <a id="whatsSuitability" />
                <div className="answer">
                  <p>
                    The quality of an XAI method cannot be judged on the basis
                    of the quality of the resulting explanation. This is highly
                    contextual and subjective due to social beliefs and
                    cognitive biases{" "}
                    <a href="https://arxiv.org/pdf/1706.07269.pdf">
                      (Miller 2017)
                    </a>
                    .{" "}
                  </p>

                  <p>
                    Accordingly, it is defined by characteristics of the context
                    of use that{" "}
                  </p>
                  <ul>
                    <li>
                      make the application of the XAI method difficult or
                      impossible
                    </li>
                    <li>
                      have a negative, distorting influence on a sound, coherent
                      and reasonable explanation result due to the algorithmic
                      nature of the XAI method{" "}
                    </li>
                    <li>
                      reduce or complicate the interpretability of the
                      explanation.{" "}
                    </li>
                  </ul>
                  <p>
                    A method rating can arise either because of (an aggregation
                    of) positive and negative criteria evaluations, or by an
                    absence of suitability-reducing criteria evaluations.{" "}
                  </p>
                  <p>
                    <b>
                      Results of the system must be seen in relative terms: Even
                      the worst rated method can be suitable if all other
                      methods were rated better due to the presence of
                      suitability-increasing criteria.
                    </b>
                  </p>
                </div>
              </Card.Body>
            </Accordion.Collapse>
          </Card>

          <Card>
            <Card.Header>
              <Accordion.Toggle
                as={Card.Header}
                variant="link"
                eventKey="howdoesitwork"
              >
                <Row className="section">
                  <Col md="1">
                    <span>
                      <AiOutlineQuestionCircle />
                    </span>
                  </Col>
                  <Col md="10">
                    <h3>How does the XAI Recommendation System work?</h3>
                  </Col>
                  <Col md="1">
                    <span>
                      <BiDownArrow />
                    </span>
                  </Col>
                </Row>
              </Accordion.Toggle>
            </Card.Header>
            <Accordion.Collapse eventKey="howdoesitwork">
              <Card.Body>
                <a id="howdoesitwork" />
                <div className="answer">
                  <p>
                    The XAI Recommender suggests you a XAI method that is the
                    most appropriate for your specific context of use.
                  </p>
                  <p>
                    Unfortunately, no exact measurement of the strength/height
                    of many input parameters is possible due to lack of
                    thresholds (e.g. “correlation”: How can you measure the
                    correlation of a complete data set?). Furthermore, the
                    literature gives only vague estimates of method suitability
                    with respect to these imprecise criteria, so only an
                    approximate recommendation is possible.
                  </p>
                  <p>
                    Therefore, the recommendation system internally uses a fuzzy
                    expert system.
                  </p>
                  <p>
                    Your crisp input, inserted via the range or the regular
                    input field, will be transformed into a literary term.
                    Depending on the truth of this term for the input value,
                    fuzzy rules are activated to determine the suitability of
                    all methods. The result of all fired rules is aggregated for
                    each method and output as a crisp value reflecting the
                    suitability of this method. So the fuzzy expert system’s
                    result is a list of XAI methods and their suitabilities.
                  </p>
                  <p>
                    In a second step, methods that cannot be applied due to
                    non-existing prerequisites, are removed from this list using
                    boolean logic. All applicable methods, sorted by their
                    suitability, will be issued!
                  </p>
                  <p>
                    The structure of the system (which can propose methods X and
                    Y) is schematically visualized in the figure below.
                  </p>
                </div>
                <div className="images">
                  <img
                    src="/images/xai_recommender_structure.png"
                    alt="Structure of XAI Recommender"
                  />
                  <p className="img-desc">
                    Schematic structure of the XAI Recommender
                  </p>
                </div>
              </Card.Body>
            </Accordion.Collapse>
          </Card>

          <Card>
            <Card.Header>
              <Accordion.Toggle
                as={Card.Header}
                variant="link"
                eventKey="availableMethods"
              >
                <Row className="section">
                  <Col md="1">
                    <span>
                      <AiOutlineQuestionCircle />
                    </span>
                  </Col>
                  <Col md="10">
                    <h3>Which XAI Methods were taken into consideration?</h3>
                  </Col>
                  <Col md="1">
                    <span>
                      <BiDownArrow />
                    </span>
                  </Col>
                </Row>
              </Accordion.Toggle>
            </Card.Header>
            <Accordion.Collapse eventKey="availableMethods">
              <Card.Body>
                <a id="availableMethods" />
                <div className="answer">
                  <BoxMethods />
                </div>
              </Card.Body>
            </Accordion.Collapse>
          </Card>

          <Card>
            <Card.Header>
              <Accordion.Toggle
                as={Card.Header}
                variant="link"
                eventKey="whichinputdata"
              >
                <Row className="section">
                  <Col md="1">
                    <span>
                      <AiOutlineQuestionCircle />
                    </span>
                  </Col>
                  <Col md="10">
                    <h3>
                      {" "}
                      Which format of input data should be taken into
                      consideration?
                    </h3>
                  </Col>
                  <Col md="1">
                    <span>
                      <BiDownArrow />
                    </span>
                  </Col>
                </Row>
              </Accordion.Toggle>
            </Card.Header>
            <Accordion.Collapse eventKey="whichinputdata">
              <Card.Body>
                <a id="whichinputdata" />
                <div className="answer">
                  <p>
                    The input of the parameters needed for the recommendation of
                    the XAI method should refer to the
                    <OverlayTrigger
                      trigger={["hover", "focus"]}
                      key="ef"
                      placement="bottom"
                      overlay={
                        <Tooltip id={`tooltip-ef`}>
                          Engineered Features are those features that have been
                          prepared for the model and its tasks and have been
                          prepared (scaled, coded, aggregated into new features)
                          from the summarized and cleaned Prepared Data using
                          the preprocessing steps.
                        </Tooltip>
                      }
                    >
                      <span className="link"> Engineered Features </span>
                    </OverlayTrigger>
                    <a href="https://cloud.google.com/solutions/machine-learning/data-preprocessing-for-ml-with-tf-transform-pt1#preprocessing_data_for_machine_learning">
                      [further information on data and preprocessing]
                    </a>
                    . These may have been subjected to
                    <OverlayTrigger
                      trigger={["hover", "focus"]}
                      key="dpp"
                      placement="bottom"
                      overlay={
                        <Tooltip id={`tooltip-dpp`}>
                          "Destructive operations" are not bijective and
                          therefore cannot be undone.From "Non-destructive
                          operations" the original representation of the feature
                          (before transformation) can be recovered.
                        </Tooltip>
                      }
                    >
                      <span className="link">
                        {" "}
                        destructive preprocessing operations{" "}
                      </span>
                    </OverlayTrigger>
                    , but should not be considered coded and unscaled.
                  </p>
                </div>
              </Card.Body>
            </Accordion.Collapse>
          </Card>

          <Card>
            <Card.Header>
              <Accordion.Toggle
                as={Card.Header}
                variant="link"
                eventKey="discrExplanation"
              >
                <Row className="section">
                  <Col md="1">
                    <span>
                      <AiOutlineQuestionCircle />
                    </span>
                  </Col>
                  <Col md="10">
                    <h3>What does the term "Discretizability" mean?</h3>
                  </Col>
                  <Col md="1">
                    <span>
                      <BiDownArrow />
                    </span>
                  </Col>
                </Row>
              </Accordion.Toggle>
            </Card.Header>
            <Accordion.Collapse eventKey="discrExplanation">
              <Card.Body>
                <a id="discrExplanation" />
                <div className="answer">
                  <p>
                    Discretizability is given if the data points of a feature
                    distribution can be divided into intervals of equal size
                    (equal-width binning) with a similar number of data points,
                    or into bins with equal frequency (e.g. deciles/quartiles)
                    with a similar width.
                  </p>
                </div>
              </Card.Body>
            </Accordion.Collapse>
          </Card>
        </Accordion>
      </Container>
    </Layout>
  )
}

export default FAQPage
