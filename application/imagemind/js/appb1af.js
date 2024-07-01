(window["webpackJsonp"] = window["webpackJsonp"] || []).push([
  ["chunk-8f249d38"],
  {
    "3cd0": function (t, e, a) {},
    "57cb": function (t, e, a) {
      t.exports = a.p + "img/organizationStructure.png";
    },
    "58cf": function (t, e, a) {
      t.exports = a.p + "img/logicalStructure.png";
    },
    "65c5": function (t, e, a) {
      "use strict";
      a("3cd0");
    },
    7992: function (t, e, a) {
      t.exports = a.p + "img/mindMap.png";
    },
    9684: function (t, e, a) {
      "use strict";
      a.r(e);
      var i = function () {
          var t = this,
            e = t._self._c;
          return e(
            "div",
            { staticClass: "page" },
            [
              e("div", { staticClass: "header" }, [
                e("div", { staticClass: "wrap" }, [
                  e("div", { staticClass: "header__wrap" }, [
                    e("div", { staticClass: "header__logo-wrap" }, [
                      e(
                        "a",
                        {
                          staticClass: "logo header__logo",
                          attrs: { href: "/" },
                        },
                        [
                          e("svg", {
                            staticClass: "logo__image",
                            attrs: {
                              viewBox: "-33.4 0 443.6 70.7",
                              height: "49",
                              width: "236",
                            },
                          }),
                        ],
                      ),
                    ]),
                    t._m(0),
                  ]),
                ]),
              ]),
              e("div", { staticClass: "inner" }, [
                e(
                  "div",
                  { staticClass: "wrap" },
                  [
                    e(
                      "div",
                      { staticClass: "ha-top" },
                      [
                        e(
                          "el-button",
                          {
                            attrs: { type: "text" },
                            on: {
                              click: function (e) {
                                t.dialogFormVisible = !0;
                              },
                            },
                          },
                          [t._v("Please Select Mind Map Structure")],
                        ),
                      ],
                      1,
                    ),
                    e(
                      "el-upload",
                      {
                        staticClass: "upload-demo",
                        attrs: {
                          drag: "",
                          action: "https://imagetomindmap.com/prod-api/upload",
                          "before-upload": t.beforeUpload,
                          "on-success": t.onSuccess,
                          "on-error": t.onError,
                          data: t.mindRequest,
                          multiple: "",
                        },
                      },
                      [
                        e("i", { staticClass: "el-icon-upload" }),
                        e("div", { staticClass: "el-upload__text" }, [
                          t._v("Drop file here or "),
                          e("em", [t._v("click to upload")]),
                        ]),
                        e(
                          "div",
                          {
                            staticClass: "el-upload__tip",
                            attrs: { slot: "tip" },
                            slot: "tip",
                          },
                          [
                            t._v(
                              "jpg/jpeg/png/bmp/gif files with a size less than 5Mb",
                            ),
                          ],
                        ),
                      ],
                    ),
                    e("div", { staticClass: "ha-bottom" }),
                    e("section", { staticClass: "inner__info" }, [
                      e(
                        "details",
                        { staticClass: "details", attrs: { open: "" } },
                        [
                          e("summary", { staticClass: "details__summary" }, [
                            e("svg", {
                              staticClass: "details__icon",
                              attrs: {
                                viewBox: "0 0 7 12",
                                width: "7",
                                height: "12",
                              },
                            }),
                            e("h1", { staticClass: "details__summary-title" }, [
                              t._v("Convert Image to Mind Map"),
                            ]),
                          ]),
                          t._m(1),
                        ],
                      ),
                      e(
                        "details",
                        { staticClass: "details", attrs: { open: "" } },
                        [
                          e("summary", { staticClass: "details__summary" }, [
                            e("svg", {
                              staticClass: "details__icon",
                              attrs: {
                                viewBox: "0 0 7 12",
                                width: "7",
                                height: "12",
                              },
                            }),
                            e("h1", { staticClass: "details__summary-title" }, [
                              t._v("How It Works"),
                            ]),
                          ]),
                          t._m(2),
                        ],
                      ),
                    ]),
                  ],
                  1,
                ),
              ]),
              e(
                "el-dialog",
                {
                  attrs: {
                    title: "Please Select Mind Map Structure",
                    visible: t.dialogFormVisible,
                    width: "384px",
                  },
                  on: {
                    "update:visible": function (e) {
                      t.dialogFormVisible = e;
                    },
                  },
                },
                [
                  e(
                    "el-row",
                    { attrs: { gutter: 20 } },
                    [
                      e("el-col", { attrs: { span: 8 } }, [
                        e(
                          "div",
                          {
                            class: { active: t.logicalStructure },
                            on: {
                              mouseenter: function (e) {
                                return t.changeLogicalStructureStyle(!0);
                              },
                              mouseleave: function (e) {
                                return t.changeLogicalStructureStyle(!1);
                              },
                              click: function (e) {
                                return t.structureCheck("logicalStructure");
                              },
                            },
                          },
                          [
                            e("el-image", {
                              staticClass: "box",
                              staticStyle: { height: "100px" },
                              attrs: { fit: "fit", src: a("58cf") },
                            }),
                          ],
                          1,
                        ),
                      ]),
                      e("el-col", { attrs: { span: 8 } }, [
                        e(
                          "div",
                          {
                            class: { active: t.mindMap },
                            on: {
                              mouseenter: function (e) {
                                return t.changeMindMapeStyle(!0);
                              },
                              mouseleave: function (e) {
                                return t.changeMindMapeStyle(!1);
                              },
                              click: function (e) {
                                return t.structureCheck("mindMap");
                              },
                            },
                          },
                          [
                            e("el-image", {
                              staticStyle: { height: "100px" },
                              attrs: { fit: "fit", src: a("7992") },
                            }),
                          ],
                          1,
                        ),
                      ]),
                      e("el-col", { attrs: { span: 8 } }, [
                        e(
                          "div",
                          {
                            class: { active: t.organizationStructure },
                            on: {
                              mouseenter: function (e) {
                                return t.changeOrganizationStructureStyle(!0);
                              },
                              mouseleave: function (e) {
                                return t.changeOrganizationStructureStyle(!1);
                              },
                              click: function (e) {
                                return t.structureCheck(
                                  "organizationStructure",
                                );
                              },
                            },
                          },
                          [
                            e("el-image", {
                              staticStyle: { height: "100px" },
                              attrs: { fit: "fit", src: a("57cb") },
                            }),
                          ],
                          1,
                        ),
                      ]),
                    ],
                    1,
                  ),
                ],
                1,
              ),
              t._m(3),
            ],
            1,
          );
        },
        s = [
          function () {
            var t = this,
              e = t._self._c;
            return e("ul", { staticClass: "menu header__menu" }, [
              e("li", { staticClass: "menu__item" }, [
                e(
                  "a",
                  {
                    staticClass: "subhead__link",
                    attrs: { href: "/imindmap" },
                  },
                  [
                    e("span", { staticClass: "subhead__link-text" }, [
                      t._v("Image2MindMap"),
                    ]),
                  ],
                ),
              ]),
            ]);
          },
          function () {
            var t = this,
              e = t._self._c;
            return e("p", { staticClass: "details__text" }, [
              t._v(
                " Image2MindMap is an innovative online tool designed to transform images into interactive mind maps.",
              ),
              e("br"),
              t._v(
                " With Image2MindMap, you can easily convert any image or diagram into a structured and organized visual representation ",
              ),
            ]);
          },
          function () {
            var t = this,
              e = t._self._c;
            return e("p", { staticClass: "details__text" }, [
              t._v("Upload Image:"),
              e("br"),
              t._v(
                " Start by uploading your image to the Image2MindMap platform.",
              ),
              e("br"),
              t._v(" Generate Mind Map:"),
              e("br"),
              t._v(
                " Once uploaded, Image2MindMap will process the image and generate a preliminary mind map structure.",
              ),
              e("br"),
              t._v(" Customize:"),
              e("br"),
              t._v(
                " Fine-tune the mind map by adding, deleting, or modifying nodes and connections as needed.",
              ),
              e("br"),
              t._v(" Export and Share:"),
              e("br"),
              t._v(
                " Export the finalized mind map to your preferred format and share it with colleagues, classmates, or friends. ",
              ),
            ]);
          },
          function () {
            var t = this,
              e = t._self._c;
            return e("div", { staticClass: "footer" }, [
              e("div", { staticClass: "wrap footer__wrap" }, [
                e("p", { staticClass: "footer__text footer__text_data" }, [
                  t._v("All uploaded data is deleted after 1 hour."),
                ]),
                e("p", { staticClass: "footer__text footer__text_copy" }, [
                  e("span", { staticClass: "footer__text-copy" }, [
                    t._v(
                      "Â© Copyright Â© 2024 Image2MindMap. All Rights Reserved.",
                    ),
                  ]),
                  e("span", { staticClass: "footer__text-line" }),
                  e(
                    "a",
                    {
                      staticClass: "footer__text-link",
                      attrs: { href: "mailto:imagetomindmap@gmail.com" },
                    },
                    [t._v("Contact Us")],
                  ),
                ]),
              ]),
            ]);
          },
        ],
        r = (a("14d9"), a("365c")),
        n = {
          methods: {
            beforeUpload(t) {
              const e =
                  "image/jpeg" === t.type ||
                  "image/jpg" === t.type ||
                  "image/png" === t.type ||
                  "image/gif" === t.type ||
                  "image/bmp" === t.type,
                a = t.size / 1024 / 1024 < 5;
              return (
                e ||
                  this.$message.error(
                    "Only supports uploading images in JPG JPEG PNG GIF BMP format",
                  ),
                a || this.$message.error("Upload image size cannot exceed 5MB"),
                "" == this.checkedStructure
                  ? (this.$message.error("Please Select Mind Map Structure"),
                    !1)
                  : e && a
              );
            },
            onSuccess(t) {
              this.$message.success(t.msg),
                0 == t.code &&
                  (Object(r["e"])(t.data.root),
                  Object(r["d"])({
                    theme: t.data.theme,
                    layout: t.data.layout,
                  }),
                  Object(r["f"])("en"),
                  this.$router.push({ name: "Mind" }));
            },
            onError(t) {
              this.$message.error("upload failed");
            },
            changeLogicalStructureStyle(t) {
              "logicalStructure" != this.checkedStructure &&
                (this.logicalStructure = t);
            },
            changeMindMapeStyle(t) {
              "mindMap" != this.checkedStructure && (this.mindMap = t);
            },
            changeOrganizationStructureStyle(t) {
              "organizationStructure" != this.checkedStructure &&
                (this.organizationStructure = t);
            },
            structureCheck(t) {
              (this.checkedStructure = t),
                (this.logicalStructure = !1),
                (this.mindMap = !1),
                (this.organizationStructure = !1),
                "logicalStructure" == t
                  ? ((this.logicalStructure = !0),
                    (this.mindRequest.mindType = 1))
                  : "mindMap" == t
                    ? ((this.mindMap = !0), (this.mindRequest.mindType = 2))
                    : "organizationStructure" == t &&
                      ((this.organizationStructure = !0),
                      (this.mindRequest.mindType = 3)),
                (this.dialogFormVisible = !1);
            },
          },
          data() {
            return {
              mindRequest: { mindType: 1 },
              logicalStructure: !1,
              mindMap: !1,
              organizationStructure: !1,
              checkedStructure: "",
              dialogFormVisible: !1,
            };
          },
        },
        o = n,
        c = (a("65c5"), a("2877")),
        l = Object(c["a"])(o, i, s, !1, null, "99647d44", null);
      e["default"] = l.exports;
    },
  },
]);
