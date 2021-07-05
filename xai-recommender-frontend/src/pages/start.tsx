import React from "react"
import axios from "axios"

import Layout from "../components/layout"
import {
  Row,
  Col,
  Container,
  Tab,
  Tabs,
  Button,
  Form,
  OverlayTrigger,
  Alert,
  Popover,
} from "react-bootstrap"
import inputConfig from "./../../static/config/frontend_input_config.json"
import { BsQuestionSquare } from "react-icons/bs"
import { Formik } from "formik"
import * as Yup from "yup"
import RecommendationContext from "../context/recommendationContext"

import "./../styles/pages/input.scss"
import { Link, navigate } from "gatsby"
import PageHeading from "../components/pageHeading"
import { BiRightArrow } from "react-icons/bi"

class StartPage extends React.Component {
  static contextType = RecommendationContext

  fieldsModel = {}
  fieldsPrefs = {}
  fieldsData = {}
  validationSchema = {}
  initialValues = {}

  static recommendationContext = RecommendationContext

  constructor(props) {
    super(props)

    this.handleSubmit = this.handleSubmit.bind(this)
    this.initializeValidationSchema = this.initializeValidationSchema.bind(this)
  }

  initializeValidationSchema() {
    var schema = {}
    var initials = {}
    Object.keys(inputConfig).map((key, idx) => {
      var config = inputConfig[key]["config"]
      // set initial values
      initials[key] = config["initialValue"]
      // schema only for numbers
      if (config["type"] == "number") {
        var min = config["min"]
        var max = config["max"]

        schema[key] = Yup.number()
          .positive()
          .min(min, `Value must be above ${min}.`)
          .max(max, `Value must be below ${max}.`)
      }
    })
    schema["model_name"] = Yup.string()
      .required(`Model name must be provided.`)
      .min(2, `Model name must be longer than 2 characters.`)
      .max(150, `Model name must be shorter than 150 characters.`)
    this.validationSchema = schema
    this.initialValues = initials

    // order input fields
    Object.keys(inputConfig).map((key, idx) => {
      var config = inputConfig[key]["config"]
      var section = config["section"] as string
      var param_type = config["param_type"] as string
      if (section == "preference") {
        this.fieldsPrefs[key] = {
          idx: idx,
          label: inputConfig[key]["label"],
          param_type: param_type,
        }
      } else if (section == "model") {
        this.fieldsModel[key] = {
          idx: idx,
          label: inputConfig[key]["label"],
          param_type: param_type,
        }
      } else {
        this.fieldsData[key] = {
          idx: idx,
          label: inputConfig[key]["label"],
          param_type: param_type,
        }
      }
    })
  }

  handleSubmit = event => {
    for (var input in event) {
      if (
        inputConfig[input] &&
        inputConfig[input]["config"]["type"] == "list"
      ) {
        // parse string to list and remove empty strings
        event[input] = event[input]
          .toString()
          .split(",")
          .map(item => item.trim())
          .filter(item => item)
      }
    }
    //console.log(event)

    axios
      .post(`${process.env.REACT_APP_BACKEND_URL}:5000/xairecommender`, event)
      .then(response => {
        console.log(response)
        this.context.changeResult(response.data)
        navigate("/result")
      })
      .catch(e => {
        console.log(e)
        if (!e.response) {
          navigate("/error")
        }
        if (e.code == 404) {
          navigate("/404")
        }
      })
  }

  checkbox(key, label, value, onChange) {
    return (
      <Form.Group as={Row} controlId={`group-${key}`} key={`k-${key}`}>
        <Col sm="10">
          <Form.Check
            custom
            key={`k-${key}`}
            type="checkbox"
            name={key}
            id={key}
            label={label}
            checked={value}
            onChange={onChange}
          />
        </Col>
        <Col sm="2">{this.helpBtn(key, label)}</Col>
      </Form.Group>
    )
  }

  helpBtn(key, label) {
    return (
      <OverlayTrigger
        trigger={["hover", "focus"]}
        key={`overlay-${key}`}
        placement="bottom"
        overlay={
          <Popover
            className={`popover-positioned-bottom`}
            id={`popover-${key}`}
          >
            <Popover.Title as="h3">{label}</Popover.Title>
            <Popover.Content>
              {inputConfig[key]["config"]["help"]}
            </Popover.Content>
          </Popover>
        }
      >
        <Button variant="light">
          <BsQuestionSquare />
        </Button>
      </OverlayTrigger>
    )
  }

  input(key, param_type, label, value, onChange, error) {
    var max = inputConfig[key]["config"]["max"]
    param_type == "list" ? "text" : param_type

    // if range, specify labels to show besides slider

    return (
      <Form.Group as={Row} controlId={`group-${key}`} key={`k-${key}`}>
        <Form.Label column sm="3">
          {label}
        </Form.Label>
        <Col sm="7">
          <div className="rangeContainer">
            {param_type == ("range" || "number") ? (
              <span className="more">
                {inputConfig[key]["config"]["range_min"]}
              </span>
            ) : null}
            <Form.Control
              className={param_type}
              name={key}
              type={param_type}
              value={value}
              min={inputConfig[key]["config"]["min"]}
              max={max}
              step={max == 1 ? "0.1" : "1"}
              //onChange={this.handleChange}
              onChange={onChange}
              isInvalid={!!error}
            />
            {param_type == ("range" || "number") ? (
              <span className="more right">
                {inputConfig[key]["config"]["range_max"]}
              </span>
            ) : null}

            <Form.Control.Feedback type="invalid">
              {error}
            </Form.Control.Feedback>
          </div>
        </Col>
        <Col sm="2">{this.helpBtn(key, label)}</Col>
      </Form.Group>
    )
  }

  checkDisplayCondition(condition) {
    if (condition instanceof Array) {
      return condition.length > 0
    } else {
      return condition ? true : false
    }
  }

  render() {
    var inputs_orig = null
    if (this.context.result) {
      var { inputs_orig } = this.context.result
    }

    // check if initialValues are set (empty when redirect without page reload)
    if (Object.keys(this.initialValues).length == 0) {
      this.initializeValidationSchema()
    }

    return (
      <Layout pageInfo={{ pageName: "Start" }}>
        <PageHeading pageTitle="Recommendation of a suitable XAI method" />
        <Container>
          <Row style={{ marginBottom: "2rem" }}>
            <Col>
              <h2>Insert values for getting a recommendation</h2>
              <p>
                In order to be able to propose the most appropriate XAI method
                for your ML model, you first of all have to provide some
                properties of your ML model and its underlying data.
                Additionally you can add personal preferences, for example
                regarding the method's explanation type or it's usage.
              </p>
              <div className="linkBox">
                <div>
                  <BiRightArrow />
                  <Link to="/faq#whyxai">Why using XAI?</Link>
                </div>
                <div>
                  <BiRightArrow />
                  <Link to="/faq#howdoesitwork">How does it work?</Link>
                </div>
              </div>
            </Col>
          </Row>
          <Row>
            <Col>
              <Formik
                validationSchema={Yup.object().shape(this.validationSchema)}
                onSubmit={this.handleSubmit}
                initialValues={inputs_orig ? inputs_orig : this.initialValues}
                enableReinitialize={true}
              >
                {/* Callback function containing Formik state and helpers that handle common form actions */}
                {({
                  values,
                  errors,
                  handleChange,
                  handleSubmit,
                  isSubmitting,
                  isValid,
                }) => (
                  <Form noValidate onSubmit={handleSubmit}>
                    <div className="formSection">
                      <h3>Model specific input parameters</h3>
                      {// render model stuff
                      Object.keys(this.fieldsModel).map((key, idx) => {
                        let display = true
                        if (inputConfig[key]["config"]["conditionalRender"]) {
                          display = this.checkDisplayCondition(
                            values[
                              inputConfig[key]["config"]["conditionalRender"]
                            ]
                          )
                            ? true
                            : false
                        }
                        if (display) {
                          var param_type = inputConfig[key]["config"][
                            "type"
                          ] as string
                          if (
                            param_type === "switch" ||
                            param_type == "checkbox"
                          ) {
                            return this.checkbox(
                              key,
                              inputConfig[key]["label"],
                              // this.state[key],
                              values[key],
                              handleChange
                            )
                          } else {
                            return this.input(
                              key,
                              param_type,
                              inputConfig[key]["label"],
                              // this.state[key],
                              values[key],
                              handleChange,
                              errors[key]
                            )
                          }
                        }
                      })}
                    </div>
                    <div className="formSection">
                      <h3>Data specific input parameters</h3>
                      <p>
                        The suitability of an XAI method highly depends on the
                        nature of the training data. Therefore, some properties
                        of these must be obtained and considered for a
                        recommendation. Several options are available for the
                        specification: An approximate specification via the tab
                        "Approximate input" is usually already sufficient.
                        However, if the required parameters are already
                        available, you can specify them in the "Exact input"
                        tab. Unfortunately, the option of automatic data
                        analysis is not yet available.
                      </p>
                      <div className="linkBox">
                        <div>
                          <BiRightArrow />
                          <Link to="/faq#whichinputdata">
                            Which format of input data should be taken into
                            consideration?
                          </Link>
                        </div>
                      </div>
                      <Tabs defaultActiveKey="input_fuzzy">
                        <Tab eventKey="input_fuzzy" title="Approximate input">
                          <h3>Approximate input</h3>
                          {Object.keys(this.fieldsData).map((key, idx) => {
                            let display = true
                            if (
                              inputConfig[key]["config"]["conditionalRender"]
                            ) {
                              display = this.checkDisplayCondition(
                                values[
                                  inputConfig[key]["config"][
                                    "conditionalRender"
                                  ]
                                ]
                              )
                                ? true
                                : false
                            }
                            if (display) {
                              var param_type = inputConfig[key]["config"][
                                "type"
                              ] as string
                              if (
                                param_type === "switch" ||
                                param_type == "checkbox"
                              ) {
                                return this.checkbox(
                                  key,
                                  inputConfig[key]["label"],
                                  // this.state[key],
                                  values[key],
                                  handleChange
                                )
                              } else {
                                // go for range input since it is fuzzy
                                return this.input(
                                  key,
                                  param_type == "number" ||
                                    param_type == "range"
                                    ? "range"
                                    : "text",
                                  inputConfig[key]["label"],
                                  values[key],
                                  handleChange,
                                  errors[key]
                                )
                              }
                            }
                          })}
                        </Tab>
                        <Tab eventKey="input_crisp" title="Exact input">
                          <h3>Exact input</h3>
                          {Object.keys(this.fieldsData).map((key, idx) => {
                            let display = true
                            if (
                              inputConfig[key]["config"]["conditionalRender"]
                            ) {
                              display = this.checkDisplayCondition(
                                values[
                                  inputConfig[key]["config"][
                                    "conditionalRender"
                                  ]
                                ]
                              )
                                ? true
                                : false
                            }
                            if (display) {
                              var param_type = inputConfig[key]["config"][
                                "type"
                              ] as string
                              if (
                                param_type === "switch" ||
                                param_type == "checkbox"
                              ) {
                                return this.checkbox(
                                  key,
                                  inputConfig[key]["label"],

                                  values[key],
                                  handleChange
                                )
                              } else {
                                // go for text input since it is crips
                                return this.input(
                                  key,
                                  param_type,
                                  inputConfig[key]["label"],
                                  // this.state[key],
                                  values[key],
                                  handleChange,
                                  errors[key]
                                )
                              }
                            }
                          })}
                        </Tab>
                        <Tab
                          eventKey="input_upload"
                          title="Automatic input by file upload"
                          disabled
                        >
                          <h2>Automatic input by file upload</h2>
                        </Tab>
                      </Tabs>
                    </div>
                    <div className="formSection">
                      <h3>User preferences regarding XAI method</h3>
                      {Object.keys(this.fieldsPrefs).map((key, idx) => {
                        var param_type = inputConfig[key]["config"][
                          "type"
                        ] as string
                        if (
                          param_type === "switch" ||
                          param_type == "checkbox"
                        ) {
                          return this.checkbox(
                            key,
                            inputConfig[key]["label"],
                            values[key],
                            handleChange
                          )
                        } else {
                          // go for range input since it is fuzzy
                          return this.input(
                            key,
                            "range",
                            inputConfig[key]["label"],
                            values[key],
                            handleChange,
                            errors[key]
                          )
                        }
                      })}
                    </div>
                    {values["foi"] == "" ? (
                      <Alert key="alert-foi" variant="warning">
                        Sure there are no Features of Interest (FOI)?
                        FOI-specific inputs will not be taken into consideration
                        without at least one feature name For further
                        considerations{" "}
                        <a href="https://www.antidiskriminierungsstelle.de/SharedDocs/Downloads/DE/publikationen/AGG/agg_gleichbehandlungsgesetz.pdf">
                          look here
                        </a>
                        .
                      </Alert>
                    ) : null}
                    <Button
                      variant="primary"
                      type="submit"
                      disabled={!isValid || isSubmitting}
                    >
                      Submit
                    </Button>
                  </Form>
                )}
              </Formik>
            </Col>
          </Row>
        </Container>
      </Layout>
    )
  }
}

export default StartPage
