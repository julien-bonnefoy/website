// TypeIt by Alex MacArthur - https://typeitjs.com
!(function (e, t) {
    "object" == typeof exports && "undefined" != typeof module ? (module.exports = t()) : "function" == typeof define && define.amd ? define(t) : ((e || self).TypeIt = t());
})(this, function () {
    const e = [null, null, {}];
    var t = (e, t) => Object.assign({}, e, t),
        n = (e) => Array.from(e),
        r = (e) => {
            let t = document.implementation.createHTMLDocument();
            return (t.body.innerHTML = e), t.body;
        };
    const o = (e, t = null, r = !1) => {
            let i = n(e.childNodes).flatMap((e) => {
                return 3 === (t = e).nodeType || "BR" === t.tagName ? e : o(e);
                var t;
            });
            return t && (i = i.filter((e) => !t.contains(e))), r ? i.reverse() : i;
        },
        i = (e, t = null) => ({ node: t, content: e });
    function s(e) {
        let t = r(e);
        return o(t).flatMap((e) => (e.nodeValue ? n(e.nodeValue).map((t) => i(t, e)) : i(e)));
    }
    function u(e, t = !0) {
        return t ? s(e) : n(e).map((e) => i(e));
    }
    var l = (e) => document.createElement(e),
        c = (e) => document.createTextNode(e),
        a = (e, t = "") => {
            let n = l("style");
            (n.id = t), n.appendChild(c(e)), document.head.appendChild(n);
        },
        f = (e) => Array.isArray(e);
    const h = (e) => Number.isInteger(e),
        d = (e, t = document, n = !1) => t["querySelector" + (n ? "All" : "")](e),
        m = "ti-cursor",
        v = "START",
        p = { started: !1, completed: !1, frozen: !1, destroyed: !1 },
        y = {
            breakLines: !0,
            cursor: !0,
            cursorChar: "|",
            cursorSpeed: 1e3,
            deleteSpeed: null,
            html: !0,
            lifeLike: !0,
            loop: !1,
            loopDelay: 750,
            nextStringDelay: 750,
            speed: 100,
            startDelay: 250,
            startDelete: !1,
            strings: [],
            waitUntilVisible: !1,
            beforeString: () => {},
            afterString: () => {},
            beforeStep: () => {},
            afterStep: () => {},
            afterComplete: () => {},
        };
    var g = ({ el: e, move: t, cursorPos: n, to: r }) =>
            h(t)
                ? -1 * t
                : ((e, t, n = v) => {
                      let r = new RegExp("END", "i").test(n),
                          i = d(".ti-cursor", t),
                          s = e ? d(e, t) : t,
                          u = o(s, i, !0),
                          l = u[0],
                          c = u[u.length - 1],
                          a = r && !e ? 0 : o(t, i, !0).findIndex((e) => e.isSameNode(r ? l : c));
                      return r && a--, a + 1;
                  })(t, e, r) - n,
        P = (e) => (f(e) || (e = [e / 2, e / 2]), e),
        b = (e, t) => Math.abs(Math.random() * (e + t - (e - t)) + (e - t));
    let N = (e) => e / 2;
    var S = (e) => "value" in e;
    const M = (e) => ("function" == typeof e ? e() : e);
    var T = (e) => "BODY" === e.tagName;
    const j = (e, t) => {
            let r = n(d("*", t, !0));
            return [t].concat(r.reverse()).find((t) => t.cloneNode().isEqualNode(e.cloneNode()));
        },
        L = (e, t, n, r) => {
            let i = t.content instanceof HTMLElement,
                s = t.node,
                u = null == s ? void 0 : s.parentNode,
                l = i ? t.content : c(t.content);
            if (S(e)) return void (e.value = "" + e.value + t.content);
            if (!i && u && !T(u)) {
                let r = j(u, e);
                if (
                    r &&
                    ((e, t) => {
                        let n = e.nextSibling;
                        return !n || n.isEqualNode(t);
                    })(r, n)
                )
                    e = r;
                else {
                    (l = u.cloneNode()), l.appendChild(c(t.content));
                    let n = u.parentNode,
                        r = n.cloneNode();
                    if (!T(n)) {
                        let t = j(r, e);
                        for (; !t && !T(n); ) {
                            let o = r;
                            (o.innerHTML = l.outerHTML), (l = o), (n = n.parentNode), (r = n.cloneNode()), (t = j(r, e));
                        }
                        e = t || e;
                    }
                }
            }
            let a = o(e, n, !0)[r - 1],
                f = a ? a.parentNode : e;
            f.insertBefore(l, f.contains(n) ? n : null);
        };
    var w = (e) => e && e.remove();
    const D = { "font-family": "", "font-weight": "", "font-size": "", "font-style": "", "line-height": "", color: "", "margin-left": "-.125em", "margin-right": ".125em" };
    function E(e, t, n) {
        if (!e.s) {
            if (n instanceof x) {
                if (!n.s) return void (n.o = E.bind(null, e, t));
                1 & t && (t = n.s), (n = n.v);
            }
            if (n && n.then) return void n.then(E.bind(null, e, t), E.bind(null, e, 2));
            (e.s = t), (e.v = n);
            const r = e.o;
            r && r(e);
        }
    }
    const x = (function () {
        function e() {}
        return (
            (e.prototype.then = function (t, n) {
                const r = new e(),
                    o = this.s;
                if (o) {
                    const e = 1 & o ? t : n;
                    if (e) {
                        try {
                            E(r, 1, e(this.v));
                        } catch (e) {
                            E(r, 2, e);
                        }
                        return r;
                    }
                    return this;
                }
                return (
                    (this.o = function (e) {
                        try {
                            const o = e.v;
                            1 & e.s ? E(r, 1, t ? t(o) : o) : n ? E(r, 1, n(o)) : E(r, 2, o);
                        } catch (e) {
                            E(r, 2, e);
                        }
                    }),
                    r
                );
            }),
            e
        );
    })();
    function k(e) {
        return e instanceof x && 1 & e.s;
    }
    function C(e, t, n) {
        var r,
            o,
            i = -1;
        return (
            (function s(u) {
                try {
                    for (; ++i < e.length && (!n || !n()); )
                        if ((u = t(i)) && u.then) {
                            if (!k(u)) return void u.then(s, o || (o = E.bind(null, (r = new x()), 2)));
                            u = u.v;
                        }
                    r ? E(r, 1, u) : (r = u);
                } catch (e) {
                    E(r || (r = new x()), 2, e);
                }
            })(),
            r
        );
    }
    function H(e, t, n) {
        for (var r; ; ) {
            var o = e();
            if ((k(o) && (o = o.v), !o)) return i;
            if (o.then) {
                r = 0;
                break;
            }
            var i = n();
            if (i && i.then) {
                if (!k(i)) {
                    r = 1;
                    break;
                }
                i = i.s;
            }
            if (t) {
                var s = t();
                if (s && s.then && !k(s)) {
                    r = 2;
                    break;
                }
            }
        }
        var u = new x(),
            l = E.bind(null, u, 2);
        return (0 === r ? o.then(a) : 1 === r ? i.then(c) : s.then(f)).then(void 0, l), u;
        function c(r) {
            i = r;
            do {
                if (t && (s = t()) && s.then && !k(s)) return void s.then(f).then(void 0, l);
                if (!(o = e()) || (k(o) && !o.v)) return void E(u, 1, i);
                if (o.then) return void o.then(a).then(void 0, l);
                k((i = n())) && (i = i.v);
            } while (!i || !i.then);
            i.then(c).then(void 0, l);
        }
        function a(e) {
            e ? ((i = n()) && i.then ? i.then(c).then(void 0, l) : c(i)) : E(u, 1, i);
        }
        function f() {
            (o = e()) ? (o.then ? o.then(a).then(void 0, l) : a(o)) : E(u, 1, i);
        }
    }
    return function (c, T = {}) {
        const j = this,
            E = this,
            x = function (e, t, n = !1) {
                try {
                    function r() {
                        function r(r) {
                            return Promise.resolve(
                                (function (e, t, n) {
                                    try {
                                        return Promise.resolve(
                                            new Promise((r) => {
                                                n.push(
                                                    setTimeout(function () {
                                                        try {
                                                            return Promise.resolve(e()).then(function () {
                                                                r();
                                                            });
                                                        } catch (e) {
                                                            return Promise.reject(e);
                                                        }
                                                    }, t)
                                                );
                                            })
                                        );
                                    } catch (e) {
                                        return Promise.reject(e);
                                    }
                                })(e, t, X)
                            ).then(function () {
                                return n ? void 0 : Promise.resolve(ee.afterStep(j)).then(function (e) {});
                            });
                        }
                        return n ? r() : Promise.resolve(ee.beforeStep(j)).then(r);
                    }
                    const o = (function () {
                        if (_.frozen)
                            return Promise.resolve(
                                new Promise((e) => {
                                    j.unfreeze = () => {
                                        (_.frozen = !1), e();
                                    };
                                })
                            ).then(function () {});
                    })();
                    return Promise.resolve(o && o.then ? o.then(r) : r());
                } catch (e) {
                    return Promise.reject(e);
                }
            },
            k = () => S(K),
            z = (e) =>
                (function (e) {
                    let { speed: t, deleteSpeed: n, lifeLike: r } = e;
                    return (n = null !== n ? n : t / 3), r ? [b(t, N(t)), b(n, N(n))] : [t, n];
                })(ee)[e],
            I = (e, t = 0) => (e ? z(t) : 0),
            B = (e, t) => (
                ne.add(e),
                ((e = {}) => {
                    let t = e.delay;
                    t && ne.add([[U, t]]);
                })(t),
                this
            ),
            R = () => ((e) => (S(e) ? n(e.value) : o(e, d(".ti-cursor", e), !0)))(K),
            A = (e = {}) => [
                [F, e],
                [F, ee],
            ],
            O = (e) => {
                let t = ee.nextStringDelay;
                ne.add([[U, t[0]], ...e, [U, t[1]]]);
            },
            V = (e) => {
                re && (oe.classList.toggle("disabled", e), oe.classList.toggle("with-delay", !e));
            },
            q = function () {
                try {
                    let e;
                    _.started = !0;
                    let t = ne.getItems();
                    const n = (function (e, n) {
                        try {
                            var r = (function () {
                                function e() {
                                    return (
                                        (_.completed = !0),
                                        Promise.resolve(ee.afterComplete(E)).then(function () {
                                            if (!ee.loop) throw "";
                                            let e = ee.loopDelay;
                                            x(function () {
                                                try {
                                                    return Promise.resolve(
                                                        (function (e) {
                                                            try {
                                                                function t(t) {
                                                                    return ne.reset(), ne.set(0, [U, e, {}]), Promise.resolve(J({ num: null })).then(function () {});
                                                                }
                                                                return Promise.resolve(Z ? Promise.resolve(Q({ value: Z })).then(t) : t());
                                                            } catch (e) {
                                                                return Promise.reject(e);
                                                            }
                                                        })(e[0])
                                                    ).then(function () {
                                                        q();
                                                    });
                                                } catch (e) {
                                                    return Promise.reject(e);
                                                }
                                            }, e[1]);
                                        })
                                    );
                                }
                                const n = C(t, function (e) {
                                    let n = t[e],
                                        r = n[2];
                                    return (
                                        r.freezeCursor && V(!0),
                                        Promise.resolve(n[0].call(E, n[1], r)).then(function () {
                                            ne.setMeta(e, { executed: !0 }), V(!1);
                                        })
                                    );
                                });
                                return n && n.then ? n.then(e) : e();
                            })();
                        } catch (e) {
                            return;
                        }
                        return r && r.then ? r.then(void 0, function () {}) : r;
                    })();
                    return Promise.resolve(
                        n && n.then
                            ? n.then(function (t) {
                                  return e ? t : E;
                              })
                            : e
                            ? n
                            : E
                    );
                } catch (e) {
                    return Promise.reject(e);
                }
            },
            U = (e = 0) => x(() => {}, e),
            Q = function ({ value: e, to: t = v, instant: n = !1 }) {
                try {
                    let r = g({ el: K, move: e, cursorPos: Z, to: t }),
                        o = () => {
                            (Z += r < 0 ? -1 : 1),
                                ((e, t, n, r) => {
                                    let o = t[Math.min(r, t.length) - 1];
                                    (e = (null == o ? void 0 : o.parentNode) || e).insertBefore(n, o || null);
                                })(K, R(), oe, Z);
                        };
                    return Promise.resolve(
                        x(function () {
                            try {
                                let e = 0;
                                const t = H(
                                    function () {
                                        return e < Math.abs(r);
                                    },
                                    function () {
                                        return e++;
                                    },
                                    function () {
                                        return n ? void o() : Promise.resolve(x(o, z(0))).then(function (e) {});
                                    }
                                );
                                return Promise.resolve(t && t.then ? t.then(function () {}) : void 0);
                            } catch (e) {
                                return Promise.reject(e);
                            }
                        }, I(n))
                    ).then(function () {});
                } catch (e) {
                    return Promise.reject(e);
                }
            },
            Y = ({ chars: e, instant: t, silent: n }) => {
                const r = this;
                return x(
                    function () {
                        try {
                            function o(o) {
                                function s() {
                                    return n ? void 0 : Promise.resolve(ee.afterString(e, r)).then(function (e) {});
                                }
                                const u = C(e, function (n) {
                                    return t
                                        ? void i(e[n])
                                        : Promise.resolve(
                                              x(() => {
                                                  i(e[n]);
                                              }, z(0))
                                          ).then(function (e) {});
                                });
                                return u && u.then ? u.then(s) : s();
                            }
                            const i = (e) => L(K, e, oe, Z);
                            return Promise.resolve(n ? o() : Promise.resolve(ee.beforeString(e, r)).then(o));
                        } catch (e) {
                            return Promise.reject(e);
                        }
                    },
                    I(t),
                    !0
                );
            },
            F = function (e) {
                try {
                    return (ee = t(ee, e)), Promise.resolve();
                } catch (e) {
                    return Promise.reject(e);
                }
            },
            G = function () {
                try {
                    return k()
                        ? ((K.value = ""), Promise.resolve())
                        : (R().forEach((e) => {
                              w(e);
                          }),
                          Promise.resolve());
                } catch (e) {
                    return Promise.reject(e);
                }
            },
            J = function ({ num: e = null, instant: t = !1, to: n = v }) {
                try {
                    return Promise.resolve(
                        x(function () {
                            try {
                                let r = h(e) ? e : g({ el: K, move: e, cursorPos: Z, to: n });
                                const o = () => {
                                    let e = R();
                                    var t;
                                    e.length &&
                                        (k()
                                            ? (K.value = K.value.slice(0, -1))
                                            : (w(e[Z]),
                                              (t = oe),
                                              d("*", K, !0).forEach((e) => {
                                                  if (!e.innerHTML && "BR" !== e.tagName && !e.isSameNode(t)) {
                                                      let t = e;
                                                      for (; 1 === t.parentElement.childNodes.length; ) t = t.parentElement;
                                                      w(t);
                                                  }
                                              })));
                                };
                                let i = 0;
                                const s = H(
                                    function () {
                                        return i < r;
                                    },
                                    function () {
                                        return i++;
                                    },
                                    function () {
                                        return t ? void o() : Promise.resolve(x(o, z(1))).then(function (e) {});
                                    }
                                );
                                return Promise.resolve(s && s.then ? s.then(function () {}) : void 0);
                            } catch (e) {
                                return Promise.reject(e);
                            }
                        }, I(t, 1))
                    ).then(function () {
                        const t = (function () {
                            if (null === e && R().length - 1 > 0) return Promise.resolve(J({ num: null })).then(function () {});
                        })();
                        if (t && t.then) return t.then(function () {});
                    });
                } catch (e) {
                    return Promise.reject(e);
                }
            };
        (this.break = function (e) {
            const t = i(l("BR"));
            return B([[Y, { chars: [t], silent: !0 }]], e);
        }),
            (this.delete = function (e = null, t = {}) {
                e = M(e);
                let n = A(t),
                    r = e,
                    { instant: o, to: i } = t;
                return B([n[0], [J, { num: r, instant: o, to: i }, $], n[1]], t);
            }),
            (this.empty = function (e = {}) {
                return B([[G]], e);
            }),
            (this.exec = function (e, t) {
                let n = A(t);
                return B([n[0], [e, null], n[1]], t);
            }),
            (this.move = function (e, t = {}) {
                e = M(e);
                let n = A(t),
                    { instant: r, to: o } = t;
                return B([n[0], [Q, { value: null === e ? "" : e, to: o, instant: r }, $], n[1]], t);
            }),
            (this.options = function (e) {
                return (e = M(e)), B([[F, e]], e);
            }),
            (this.pause = function (e, t = {}) {
                return B([[U, M(e)]], t);
            }),
            (this.type = function (e, t = {}) {
                e = M(e);
                let n = A(t),
                    r = u(e, ee.html),
                    { instant: o } = t;
                return B([n[0], [Y, { chars: r, instant: o }, $], n[1]], t);
            }),
            (this.is = function (e) {
                return _[e];
            }),
            (this.destroy = function (e = !0) {
                X.forEach((e) => clearTimeout(e)), (X = []), M(e) && w(oe), (_.destroyed = !0);
            }),
            (this.freeze = function () {
                _.frozen = !0;
            }),
            (this.unfreeze = function () {}),
            (this.reset = function () {
                !this.is("destroyed") && this.destroy(), ne.reset(), (Z = 0);
                for (let e in _) _[e] = !1;
                return (K[k() ? "value" : "innerHTML"] = ""), this;
            }),
            (this.go = function () {
                return _.started
                    ? this
                    : ((function () {
                          try {
                              !k() && K.appendChild(oe),
                                  re
                                      ? (((e, t, n) => {
                                            let r = "[data-typeit-id='" + e + "'] ." + m,
                                                o = getComputedStyle(n),
                                                i = Object.entries(D).reduce((e, [t, n]) => e + " " + t + ": var(--ti-" + t + ", " + (n || o[t]) + ");", "");
                                            a(
                                                "@keyframes blink-" +
                                                    e +
                                                    " { 0% {opacity: 0} 49% {opacity: 0} 50% {opacity: 1} } " +
                                                    r +
                                                    " { display: inline; letter-spacing: -1em; " +
                                                    i +
                                                    " animation: blink-" +
                                                    e +
                                                    " " +
                                                    t.cursorSpeed / 1e3 +
                                                    "s infinite; } " +
                                                    r +
                                                    ".with-delay { animation-delay: 500ms; } " +
                                                    r +
                                                    ".disabled { animation: none; }",
                                                e
                                            );
                                        })(te, ee, K),
                                        Promise.resolve())
                                      : Promise.resolve();
                          } catch (e) {
                              return Promise.reject(e);
                          }
                      })(),
                      ee.waitUntilVisible
                          ? (((e, t) => {
                                new IntersectionObserver(
                                    (n, r) => {
                                        n.forEach((n) => {
                                            n.isIntersecting && (t(), r.unobserve(e));
                                        });
                                    },
                                    { threshold: 1 }
                                ).observe(e);
                            })(K, q.bind(this)),
                            this)
                          : (q(), this));
            }),
            (this.getQueue = function () {
                return ne;
            }),
            (this.getOptions = function () {
                return ee;
            }),
            (this.getElement = function () {
                return K;
            });
        let K = "string" == typeof (W = c) ? d(W) : W;
        var W;
        let X = [],
            Z = 0,
            $ = { freezeCursor: !0 },
            _ = t({}, p),
            ee = t(y, T);
        ee = t(ee, { html: !k() && ee.html, nextStringDelay: P(ee.nextStringDelay), loopDelay: P(ee.loopDelay) });
        let te = Math.random().toString().substring(2, 9),
            ne = (function (n) {
                const r = function (t) {
                    return (o = o.concat(t.map((t) => e.map((e, n) => (t[n] ? t[n] : e))))), this;
                };
                let o = [];
                return (
                    r(n),
                    {
                        add: r,
                        set: function (e, t) {
                            o[e] = t;
                        },
                        reset: function () {
                            o = o.map((e) => ((e[2].executed = !1), e));
                        },
                        getItems: function () {
                            return o.filter((e) => !e[2].executed);
                        },
                        setMeta: function (e, n) {
                            o[e][2] = t(o[e][2], n);
                        },
                    }
                );
            })([[U, ee.startDelay]]);
        (K.dataset.typeitId = te), a("[data-typeit-id]:before {content: '.'; display: inline-block; width: 0; visibility: hidden;}");
        let re = ee.cursor && !k(),
            oe = (() => {
                if (k()) return;
                let e = l("span");
                return (e.className = m), re ? ((e.innerHTML = r(ee.cursorChar).innerHTML), e) : ((e.style.visibility = "hidden"), e);
            })();
        var ie;
        (ee.strings = ((e) => {
            let t = K.innerHTML;
            return t
                ? ((K.innerHTML = ""),
                  ee.startDelete
                      ? (s(t).forEach((e) => {
                            L(K, e, oe, Z);
                        }),
                        O([[J, { num: null }]]),
                        e)
                      : t
                            .trim()
                            .split(/<br(?:\s*?)(?:\/)?>/)
                            .concat(e))
                : e;
        })(f((ie = ee.strings)) ? ie : [ie])),
            ee.strings.length &&
                (() => {
                    let e = ee.strings.filter((e) => !!e);
                    e.forEach((t, n) => {
                        let r = u(t, ee.html);
                        if ((ne.add([[Y, { chars: r }, $]]), n + 1 === e.length)) return;
                        const o = ee.breakLines ? [[Y, { chars: [i(l("BR"))], silent: !0 }, $]] : [[J, { num: r.length }, $]];
                        O(o);
                    });
                })();
    };
});
