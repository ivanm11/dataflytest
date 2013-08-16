/*!
 * CanJS - 1.1.6
 * http://canjs.us/
 * Copyright (c) 2013 Bitovi
 * Wed, 24 Jul 2013 13:51:48 GMT
 * Licensed MIT
 * Includes: can/construct/construct.js,can/observe/observe.js,can/control/control.js,can/route/route.js,can/construct/super/super.js,can/construct/proxy/proxy.js,can/control/plugin/plugin.js,can/util/string/string.js
 * Download from: http://bitbuilder.herokuapp.com/can.custom.js?configuration=jquery&plugins=can%2Fconstruct%2Fconstruct.js&plugins=can%2Fobserve%2Fobserve.js&plugins=can%2Fcontrol%2Fcontrol.js&plugins=can%2Froute%2Froute.js&plugins=can%2Fconstruct%2Fsuper%2Fsuper.js&plugins=can%2Fconstruct%2Fproxy%2Fproxy.js&plugins=can%2Fcontrol%2Fplugin%2Fplugin.js&plugins=can%2Futil%2Fstring%2Fstring.js
 */
(function(undefined) {

    // ## can/util/can.js
    var __m5 = (function() {
        var can = window.can || {};
        if (typeof GLOBALCAN === 'undefined' || GLOBALCAN !== false) {
            window.can = can;
        }

        can.isDeferred = function(obj) {
            var isFunction = this.isFunction;
            // Returns `true` if something looks like a deferred.
            return obj && isFunction(obj.then) && isFunction(obj.pipe);
        };

        var cid = 0;
        can.cid = function(object, name) {
            if (object._cid) {
                return object._cid
            } else {
                return object._cid = (name || "") + (++cid)
            }
        }
        can.VERSION = '@EDGE';
        return can;
    })();

    // ## can/util/array/each.js
    var __m6 = (function(can) {
        can.each = function(elements, callback, context) {
            var i = 0,
                key;
            if (elements) {
                if (typeof elements.length === 'number' && elements.pop) {
                    if (elements.attr) {
                        elements.attr('length');
                    }
                    for (key = elements.length; i < key; i++) {
                        if (callback.call(context || elements[i], elements[i], i, elements) === false) {
                            break;
                        }
                    }
                } else if (elements.hasOwnProperty) {
                    for (key in elements) {
                        if (elements.hasOwnProperty(key)) {
                            if (callback.call(context || elements[key], elements[key], key, elements) === false) {
                                break;
                            }
                        }
                    }
                }
            }
            return elements;
        };

        return can;
    })(__m5);

    // ## can/util/jquery/jquery.js
    var __m3 = (function($, can) {
        // _jQuery node list._
        $.extend(can, $, {
                trigger: function(obj, event, args) {
                    if (obj.trigger) {
                        obj.trigger(event, args);
                    } else {
                        $.event.trigger(event, args, obj, true);
                    }
                },
                addEvent: function(ev, cb) {
                    $([this]).bind(ev, cb);
                    return this;
                },
                removeEvent: function(ev, cb) {
                    $([this]).unbind(ev, cb);
                    return this;
                },
                // jquery caches fragments, we always needs a new one
                buildFragment: function(elems, context) {
                    var oldFragment = $.buildFragment,
                        ret;

                    elems = [elems];
                    // Set context per 1.8 logic
                    context = context || document;
                    context = !context.nodeType && context[0] || context;
                    context = context.ownerDocument || context;

                    ret = oldFragment.call(jQuery, elems, context);

                    return ret.cacheable ? $.clone(ret.fragment) : ret.fragment || ret;
                },
                $: $,
                each: can.each
            });

        // Wrap binding functions.
        $.each(['bind', 'unbind', 'undelegate', 'delegate'], function(i, func) {
            can[func] = function() {
                var t = this[func] ? this : $([this]);
                t[func].apply(t, arguments);
                return this;
            };
        });

        // Wrap modifier functions.
        $.each(["append", "filter", "addClass", "remove", "data", "get"], function(i, name) {
            can[name] = function(wrapped) {
                return wrapped[name].apply(wrapped, can.makeArray(arguments).slice(1));
            };
        });

        // Memory safe destruction.
        var oldClean = $.cleanData;

        $.cleanData = function(elems) {
            $.each(elems, function(i, elem) {
                if (elem) {
                    can.trigger(elem, "destroyed", [], false);
                }
            });
            oldClean(elems);
        };

        return can;
    })(jQuery, __m5, __m6);

    // ## can/util/string/string.js
    var __m2 = (function(can) {
        // ##string.js
        // _Miscellaneous string utility functions._  

        // Several of the methods in this plugin use code adapated from Prototype
        // Prototype JavaScript framework, version 1.6.0.1.
        // © 2005-2007 Sam Stephenson
        var strUndHash = /_|-/,
            strColons = /\=\=/,
            strWords = /([A-Z]+)([A-Z][a-z])/g,
            strLowUp = /([a-z\d])([A-Z])/g,
            strDash = /([a-z\d])([A-Z])/g,
            strReplacer = /\{([^\}]+)\}/g,
            strQuote = /"/g,
            strSingleQuote = /'/g,

            // Returns the `prop` property from `obj`.
            // If `add` is true and `prop` doesn't exist in `obj`, create it as an
            // empty object.
            getNext = function(obj, prop, add) {
                var result = obj[prop];

                if (result === undefined && add === true) {
                    result = obj[prop] = {}
                }
                return result
            },

            // Returns `true` if the object can have properties (no `null`s).
            isContainer = function(current) {
                return (/^f|^o/).test(typeof current);
            };

        can.extend(can, {
                // Escapes strings for HTML.

                esc: function(content) {
                    // Convert bad values into empty strings
                    var isInvalid = content === null || content === undefined || (isNaN(content) && ("" + content === 'NaN'));
                    return ("" + (isInvalid ? '' : content))
                        .replace(/&/g, '&amp;')
                        .replace(/</g, '&lt;')
                        .replace(/>/g, '&gt;')
                        .replace(strQuote, '&#34;')
                        .replace(strSingleQuote, "&#39;");
                },


                getObject: function(name, roots, add) {

                    // The parts of the name we are looking up
                    // `['App','Models','Recipe']`
                    var parts = name ? name.split('.') : [],
                        length = parts.length,
                        current,
                        r = 0,
                        i, container, rootsLength;

                    // Make sure roots is an `array`.
                    roots = can.isArray(roots) ? roots : [roots || window];

                    rootsLength = roots.length

                    if (!length) {
                        return roots[0];
                    }

                    // For each root, mark it as current.
                    for (r; r < rootsLength; r++) {
                        current = roots[r];
                        container = undefined;

                        // Walk current to the 2nd to last object or until there
                        // is not a container.
                        for (i = 0; i < length && isContainer(current); i++) {
                            container = current;
                            current = getNext(container, parts[i]);
                        }

                        // If we found property break cycle
                        if (container !== undefined && current !== undefined) {
                            break
                        }
                    }

                    // Remove property from found container
                    if (add === false && current !== undefined) {
                        delete container[parts[i - 1]]
                    }

                    // When adding property add it to the first root
                    if (add === true && current === undefined) {
                        current = roots[0]

                        for (i = 0; i < length && isContainer(current); i++) {
                            current = getNext(current, parts[i], true);
                        }
                    }

                    return current;
                },
                // Capitalizes a string.

                capitalize: function(s, cache) {
                    // Used to make newId.
                    return s.charAt(0).toUpperCase() + s.slice(1);
                },

                // Underscores a string.

                underscore: function(s) {
                    return s
                        .replace(strColons, '/')
                        .replace(strWords, '$1_$2')
                        .replace(strLowUp, '$1_$2')
                        .replace(strDash, '_')
                        .toLowerCase();
                },
                // Micro-templating.

                sub: function(str, data, remove) {
                    var obs = [];

                    str = str || '';

                    obs.push(str.replace(strReplacer, function(whole, inside) {

                                // Convert inside to type.
                                var ob = can.getObject(inside, data, remove === true ? false : undefined);

                                if (ob === undefined) {
                                    obs = null;
                                    return "";
                                }

                                // If a container, push into objs (which will return objects found).
                                if (isContainer(ob) && obs) {
                                    obs.push(ob);
                                    return "";
                                }

                                return "" + ob;
                            }));

                    return obs === null ? obs : (obs.length <= 1 ? obs[0] : obs);
                },

                // These regex's are used throughout the rest of can, so let's make
                // them available.
                replacer: strReplacer,
                undHash: strUndHash
            });
        return can;
    })(__m3);

    // ## can/construct/construct.js
    var __m1 = (function(can) {

        // ## construct.js
        // `can.Construct`  
        // _This is a modified version of
        // [John Resig's class](http://ejohn.org/blog/simple-javascript-inheritance/).  
        // It provides class level inheritance and callbacks._

        // A private flag used to initialize a new class instance without
        // initializing it's bindings.
        var initializing = 0;


        can.Construct = function() {
            if (arguments.length) {
                return can.Construct.extend.apply(can.Construct, arguments);
            }
        };


        can.extend(can.Construct, {

                newInstance: function() {
                    // Get a raw instance object (`init` is not called).
                    var inst = this.instance(),
                        arg = arguments,
                        args;

                    // Call `setup` if there is a `setup`
                    if (inst.setup) {
                        args = inst.setup.apply(inst, arguments);
                    }

                    // Call `init` if there is an `init`  
                    // If `setup` returned `args`, use those as the arguments
                    if (inst.init) {
                        inst.init.apply(inst, args || arguments);
                    }

                    return inst;
                },
                // Overwrites an object with methods. Used in the `super` plugin.
                // `newProps` - New properties to add.  
                // `oldProps` - Where the old properties might be (used with `super`).  
                // `addTo` - What we are adding to.
                _inherit: function(newProps, oldProps, addTo) {
                    can.extend(addTo || newProps, newProps || {})
                },
                // used for overwriting a single property.
                // this should be used for patching other objects
                // the super plugin overwrites this
                _overwrite: function(what, oldProps, propName, val) {
                    what[propName] = val;
                },
                // Set `defaults` as the merger of the parent `defaults` and this 
                // object's `defaults`. If you overwrite this method, make sure to
                // include option merging logic.

                setup: function(base, fullName) {
                    this.defaults = can.extend(true, {}, base.defaults, this.defaults);
                },
                // Create's a new `class` instance without initializing by setting the
                // `initializing` flag.
                instance: function() {

                    // Prevents running `init`.
                    initializing = 1;

                    var inst = new this();

                    // Allow running `init`.
                    initializing = 0;

                    return inst;
                },
                // Extends classes.

                extend: function(fullName, klass, proto) {
                    // Figure out what was passed and normalize it.
                    if (typeof fullName != 'string') {
                        proto = klass;
                        klass = fullName;
                        fullName = null;
                    }

                    if (!proto) {
                        proto = klass;
                        klass = null;
                    }
                    proto = proto || {};

                    var _super_class = this,
                        _super = this.prototype,
                        name, shortName, namespace, prototype;

                    // Instantiate a base class (but only create the instance,
                    // don't run the init constructor).
                    prototype = this.instance();

                    // Copy the properties over onto the new prototype.
                    can.Construct._inherit(proto, _super, prototype);

                    // The dummy class constructor.

                    function Constructor() {
                        // All construction is actually done in the init method.
                        if (!initializing) {
                            return this.constructor !== Constructor && arguments.length ?
                            // We are being called without `new` or we are extending.
                            arguments.callee.extend.apply(arguments.callee, arguments) :
                            // We are being called with `new`.
                            this.constructor.newInstance.apply(this.constructor, arguments);
                        }
                    }

                    // Copy old stuff onto class (can probably be merged w/ inherit)
                    for (name in _super_class) {
                        if (_super_class.hasOwnProperty(name)) {
                            Constructor[name] = _super_class[name];
                        }
                    }

                    // Copy new static properties on class.
                    can.Construct._inherit(klass, _super_class, Constructor);

                    // Setup namespaces.
                    if (fullName) {

                        var parts = fullName.split('.'),
                            shortName = parts.pop(),
                            current = can.getObject(parts.join('.'), window, true),
                            namespace = current,
                            _fullName = can.underscore(fullName.replace(/\./g, "_")),
                            _shortName = can.underscore(shortName);



                        current[shortName] = Constructor;
                    }

                    // Set things that shouldn't be overwritten.
                    can.extend(Constructor, {
                            constructor: Constructor,
                            prototype: prototype,

                            namespace: namespace,

                            _shortName: _shortName,

                            fullName: fullName,
                            _fullName: _fullName
                        });

                    // Dojo and YUI extend undefined
                    if (shortName !== undefined) {
                        Constructor.shortName = shortName;
                    }

                    // Make sure our prototype looks nice.
                    Constructor.prototype.constructor = Constructor;


                    // Call the class `setup` and `init`
                    var t = [_super_class].concat(can.makeArray(arguments)),
                        args = Constructor.setup.apply(Constructor, t);

                    if (Constructor.init) {
                        Constructor.init.apply(Constructor, args || t);
                    }


                    return Constructor;

                }

            });
        return can.Construct;
    })(__m2);

    // ## can/util/bind/bind.js
    var __m8 = (function(can) {


        // ## Bind helpers
        can.bindAndSetup = function() {
            // Add the event to this object
            can.addEvent.apply(this, arguments);
            // If not initializing, and the first binding
            // call bindsetup if the function exists.
            if (!this._init) {
                if (!this._bindings) {
                    this._bindings = 1;
                    // setup live-binding
                    this._bindsetup && this._bindsetup();

                } else {
                    this._bindings++;
                }

            }

            return this;
        };

        can.unbindAndTeardown = function(ev, handler) {
            // Remove the event handler
            can.removeEvent.apply(this, arguments);

            this._bindings--;
            // If there are no longer any bindings and
            // there is a bindteardown method, call it.
            if (!this._bindings) {
                this._bindteardown && this._bindteardown();
            }
            return this;
        }

        return can;

    })(__m3);

    // ## can/observe/observe.js
    var __m7 = (function(can, bind) {
        // ## observe.js  
        // `can.Observe`  
        // _Provides the observable pattern for JavaScript Objects._  
        // Returns `true` if something is an object with properties of its own.
        var canMakeObserve = function(obj) {
            return obj && !can.isDeferred(obj) && (can.isArray(obj) || can.isPlainObject(obj) || (obj instanceof can.Observe));
        },

            // Removes all listeners.
            unhookup = function(items, namespace) {
                return can.each(items, function(item) {
                    if (item && item.unbind) {
                        item.unbind("change" + namespace);
                    }
                });
            },
            // Listens to changes on `child` and "bubbles" the event up.  
            // `child` - The object to listen for changes on.  
            // `prop` - The property name is at on.  
            // `parent` - The parent object of prop.
            // `ob` - (optional) The Observe object constructor
            // `list` - (optional) The observable list constructor
            hookupBubble = function(child, prop, parent, Ob, List) {
                Ob = Ob || Observe;
                List = List || Observe.List;

                // If it's an `array` make a list, otherwise a child.
                if (child instanceof Observe) {
                    // We have an `observe` already...
                    // Make sure it is not listening to this already
                    // It's only listening if it has bindings already.
                    parent._bindings && unhookup([child], parent._cid);
                } else if (can.isArray(child)) {
                    child = new List(child);
                } else {
                    child = new Ob(child);
                }
                // only listen if something is listening to you
                if (parent._bindings) {
                    // Listen to all changes and `batchTrigger` upwards.
                    bindToChildAndBubbleToParent(child, prop, parent)
                }


                return child;
            },
            bindToChildAndBubbleToParent = function(child, prop, parent) {
                child.bind("change" + parent._cid, function() {
                    // `batchTrigger` the type on this...
                    var args = can.makeArray(arguments),
                        ev = args.shift();
                    args[0] = (prop === "*" ? [parent.indexOf(child), args[0]] : [prop, args[0]]).join(".");

                    // track objects dispatched on this observe		
                    ev.triggeredNS = ev.triggeredNS || {};

                    // if it has already been dispatched exit
                    if (ev.triggeredNS[parent._cid]) {
                        return;
                    }

                    ev.triggeredNS[parent._cid] = true;
                    // send change event with modified attr to parent	
                    can.trigger(parent, ev, args);
                    // send modified attr event to parent
                    //can.trigger(parent, args[0], args);
                });
            }
            // An `id` to track events for a given observe.
        observeId = 0,
        // A helper used to serialize an `Observe` or `Observe.List`.  
        // `observe` - The observable.  
        // `how` - To serialize with `attr` or `serialize`.  
        // `where` - To put properties, in an `{}` or `[]`.
        serialize = function(observe, how, where) {
            // Go through each property.
            observe.each(function(val, name) {
                // If the value is an `object`, and has an `attrs` or `serialize` function.
                where[name] = canMakeObserve(val) && can.isFunction(val[how]) ?
                // Call `attrs` or `serialize` to get the original data back.
                val[how]() :
                // Otherwise return the value.
                val;
            });
            return where;
        },
        attrParts = function(attr, keepKey) {
            if (keepKey) {
                return [attr];
            }
            return can.isArray(attr) ? attr : ("" + attr).split(".");
        },
        // Which batch of events this is for -- might not want to send multiple
        // messages on the same batch.  This is mostly for event delegation.
        batchNum = 1,
        // how many times has start been called without a stop
        transactions = 0,
        // an array of events within a transaction
        batchEvents = [],
        stopCallbacks = [],
        makeBindSetup = function(wildcard) {
            return function() {
                var parent = this;
                this._each(function(child, prop) {
                    if (child && child.bind) {
                        bindToChildAndBubbleToParent(child, wildcard || prop, parent)
                    }
                })
            };
        };


        var Observe = can.Map = can.Observe = can.Construct({

                // keep so it can be overwritten
                bind: can.bindAndSetup,
                unbind: can.unbindAndTeardown,
                id: "id",
                canMakeObserve: canMakeObserve,
                // starts collecting events
                // takes a callback for after they are updated
                // how could you hook into after ejs

                startBatch: function(batchStopHandler) {
                    transactions++;
                    batchStopHandler && stopCallbacks.push(batchStopHandler);
                },

                stopBatch: function(force, callStart) {
                    if (force) {
                        transactions = 0;
                    } else {
                        transactions--;
                    }

                    if (transactions == 0) {
                        var items = batchEvents.slice(0),
                            callbacks = stopCallbacks.slice(0);
                        batchEvents = [];
                        stopCallbacks = [];
                        batchNum++;
                        callStart && this.startBatch();
                        can.each(items, function(args) {
                            can.trigger.apply(can, args);
                        });
                        can.each(callbacks, function(cb) {
                            cb();
                        });
                    }
                },

                triggerBatch: function(item, event, args) {
                    // Don't send events if initalizing.
                    if (!item._init) {
                        if (transactions == 0) {
                            return can.trigger(item, event, args);
                        } else {
                            event = typeof event === "string" ? {
                                type: event
                            } :
                                event;
                            event.batchNum = batchNum;
                            batchEvents.push([
                                    item,
                                    event,
                                    args
                                ]);
                        }
                    }
                },

                keys: function(observe) {
                    var keys = [];
                    Observe.__reading && Observe.__reading(observe, '__keys');
                    for (var keyName in observe._data) {
                        keys.push(keyName);
                    }
                    return keys;
                }
            },

            {
                setup: function(obj) {
                    // `_data` is where we keep the properties.
                    this._data = {};

                    // The namespace this `object` uses to listen to events.
                    can.cid(this, ".observe");
                    // Sets all `attrs`.
                    this._init = 1;
                    this.attr(obj);
                    this.bind('change' + this._cid, can.proxy(this._changes, this));
                    delete this._init;
                },
                _bindsetup: makeBindSetup(),
                _bindteardown: function() {
                    var cid = this._cid;
                    this._each(function(child) {
                        unhookup([child], cid)
                    })
                },
                _changes: function(ev, attr, how, newVal, oldVal) {
                    Observe.triggerBatch(this, {
                            type: attr,
                            batchNum: ev.batchNum
                        }, [newVal, oldVal]);
                },
                _triggerChange: function(attr, how, newVal, oldVal) {
                    Observe.triggerBatch(this, "change", can.makeArray(arguments))
                },
                // no live binding iterator
                _each: function(callback) {
                    var data = this.__get();
                    for (var prop in data) {
                        if (data.hasOwnProperty(prop)) {
                            callback(data[prop], prop)
                        }
                    }
                },

                attr: function(attr, val) {
                    // This is super obfuscated for space -- basically, we're checking
                    // if the type of the attribute is not a `number` or a `string`.
                    var type = typeof attr;
                    if (type !== "string" && type !== "number") {
                        return this._attrs(attr, val)
                    } else if (arguments.length === 1) { // If we are getting a value.
                        // Let people know we are reading.
                        Observe.__reading && Observe.__reading(this, attr)
                        return this._get(attr)
                    } else {
                        // Otherwise we are setting.
                        this._set(attr, val);
                        return this;
                    }
                },

                each: function() {
                    Observe.__reading && Observe.__reading(this, '__keys');
                    return can.each.apply(undefined, [this.__get()].concat(can.makeArray(arguments)))
                },

                removeAttr: function(attr) {
                    // Info if this is List or not
                    var isList = this instanceof can.Observe.List,
                        // Convert the `attr` into parts (if nested).
                        parts = attrParts(attr),
                        // The actual property to remove.
                        prop = parts.shift(),
                        // The current value.
                        current = isList ? this[prop] : this._data[prop];

                    // If we have more parts, call `removeAttr` on that part.
                    if (parts.length) {
                        return current.removeAttr(parts)
                    } else {
                        if (isList) {
                            this.splice(prop, 1)
                        } else if (prop in this._data) {
                            // Otherwise, `delete`.
                            delete this._data[prop];
                            // Create the event.
                            if (!(prop in this.constructor.prototype)) {
                                delete this[prop]
                            }
                            // Let others know the number of keys have changed
                            Observe.triggerBatch(this, "__keys");
                            this._triggerChange(prop, "remove", undefined, current);

                        }
                        return current;
                    }
                },
                // Reads a property from the `object`.
                _get: function(attr) {
                    var value = typeof attr === 'string' && !! ~attr.indexOf('.') && this.__get(attr);
                    if (value) {
                        return value;
                    }

                    // break up the attr (`"foo.bar"`) into `["foo","bar"]`
                    var parts = attrParts(attr),
                        // get the value of the first attr name (`"foo"`)
                        current = this.__get(parts.shift());
                    // if there are other attributes to read
                    return parts.length ?
                    // and current has a value
                    current ?
                    // lookup the remaining attrs on current
                    current._get(parts) :
                    // or if there's no current, return undefined
                    undefined :
                    // if there are no more parts, return current
                    current;
                },
                // Reads a property directly if an `attr` is provided, otherwise
                // returns the "real" data object itself.
                __get: function(attr) {
                    return attr ? this._data[attr] : this._data;
                },
                // Sets `attr` prop as value on this object where.
                // `attr` - Is a string of properties or an array  of property values.
                // `value` - The raw value to set.
                _set: function(attr, value, keepKey) {
                    // Convert `attr` to attr parts (if it isn't already).
                    var parts = attrParts(attr, keepKey),
                        // The immediate prop we are setting.
                        prop = parts.shift(),
                        // The current value.
                        current = this.__get(prop);

                    // If we have an `object` and remaining parts.
                    if (canMakeObserve(current) && parts.length) {
                        // That `object` should set it (this might need to call attr).
                        current._set(parts, value)
                    } else if (!parts.length) {
                        // We're in "real" set territory.
                        if (this.__convert) {
                            value = this.__convert(prop, value)
                        }
                        this.__set(prop, value, current)
                    } else {
                        throw "can.Observe: Object does not exist"
                    }
                },
                __set: function(prop, value, current) {

                    // Otherwise, we are setting it on this `object`.
                    // TODO: Check if value is object and transform
                    // are we changing the value.
                    if (value !== current) {
                        // Check if we are adding this for the first time --
                        // if we are, we need to create an `add` event.
                        var changeType = this.__get().hasOwnProperty(prop) ? "set" : "add";

                        // Set the value on data.
                        this.___set(prop,

                            // If we are getting an object.
                            canMakeObserve(value) ?

                            // Hook it up to send event.
                            hookupBubble(value, prop, this) :
                            // Value is normal.
                            value);

                        if (changeType == "add") {
                            // If there is no current value, let others know that
                            // the the number of keys have changed

                            Observe.triggerBatch(this, "__keys", undefined);

                        }
                        // `batchTrigger` the change event.
                        this._triggerChange(prop, changeType, value, current);

                        //Observe.triggerBatch(this, prop, [value, current]);
                        // If we can stop listening to our old value, do it.
                        current && unhookup([current], this._cid);
                    }

                },
                // Directly sets a property on this `object`.
                ___set: function(prop, val) {
                    this._data[prop] = val;
                    // Add property directly for easy writing.
                    // Check if its on the `prototype` so we don't overwrite methods like `attrs`.
                    if (!(prop in this.constructor.prototype)) {
                        this[prop] = val
                    }
                },


                bind: can.bindAndSetup,

                unbind: can.unbindAndTeardown,

                serialize: function() {
                    return serialize(this, 'serialize', {});
                },

                _attrs: function(props, remove) {

                    if (props === undefined) {
                        return serialize(this, 'attr', {})
                    }

                    props = can.extend({}, props);
                    var prop,
                        self = this,
                        newVal;
                    Observe.startBatch();
                    this.each(function(curVal, prop) {
                        newVal = props[prop];

                        // If we are merging...
                        if (newVal === undefined) {
                            remove && self.removeAttr(prop);
                            return;
                        }

                        if (self.__convert) {
                            newVal = self.__convert(prop, newVal)
                        }

                        // if we're dealing with models, want to call _set to let converter run
                        if (newVal instanceof can.Observe) {
                            self.__set(prop, newVal, curVal)
                            // if its an object, let attr merge
                        } else if (canMakeObserve(curVal) && canMakeObserve(newVal) && curVal.attr) {
                            curVal.attr(newVal, remove)
                            // otherwise just set
                        } else if (curVal != newVal) {
                            self.__set(prop, newVal, curVal)
                        }

                        delete props[prop];
                    })
                    // Add remaining props.
                    for (var prop in props) {
                        newVal = props[prop];
                        this._set(prop, newVal, true)
                    }
                    Observe.stopBatch()
                    return this;
                },


                compute: function(prop) {
                    return can.compute(this, prop);
                }
            });
        // Helpers for `observable` lists.
        var splice = [].splice,

            list = Observe(

                {
                    setup: function(instances, options) {
                        this.length = 0;
                        can.cid(this, ".observe")
                        this._init = 1;
                        if (can.isDeferred(instances)) {
                            this.replace(instances)
                        } else {
                            this.push.apply(this, can.makeArray(instances || []));
                        }
                        // this change needs to be ignored
                        this.bind('change' + this._cid, can.proxy(this._changes, this));
                        can.extend(this, options);
                        delete this._init;
                    },
                    _triggerChange: function(attr, how, newVal, oldVal) {

                        Observe.prototype._triggerChange.apply(this, arguments)
                        // `batchTrigger` direct add and remove events...
                        if (!~attr.indexOf('.')) {

                            if (how === 'add') {
                                Observe.triggerBatch(this, how, [newVal, +attr]);
                                Observe.triggerBatch(this, 'length', [this.length]);
                            } else if (how === 'remove') {
                                Observe.triggerBatch(this, how, [oldVal, +attr]);
                                Observe.triggerBatch(this, 'length', [this.length]);
                            } else {
                                Observe.triggerBatch(this, how, [newVal, +attr])
                            }

                        }

                    },
                    __get: function(attr) {
                        return attr ? this[attr] : this;
                    },
                    ___set: function(attr, val) {
                        this[attr] = val;
                        if (+attr >= this.length) {
                            this.length = (+attr + 1)
                        }
                    },
                    _each: function(callback) {
                        var data = this.__get();
                        for (var i = 0; i < data.length; i++) {
                            callback(data[i], i)
                        }
                    },
                    _bindsetup: makeBindSetup("*"),
                    // Returns the serialized form of this list.

                    serialize: function() {
                        return serialize(this, 'serialize', []);
                    },

                    splice: function(index, howMany) {
                        var args = can.makeArray(arguments),
                            i;

                        for (i = 2; i < args.length; i++) {
                            var val = args[i];
                            if (canMakeObserve(val)) {
                                args[i] = hookupBubble(val, "*", this, this.constructor.Observe, this.constructor)
                            }
                        }
                        if (howMany === undefined) {
                            howMany = args[1] = this.length - index;
                        }
                        var removed = splice.apply(this, args);
                        can.Observe.startBatch();
                        if (howMany > 0) {
                            this._triggerChange("" + index, "remove", undefined, removed);
                            unhookup(removed, this._cid);
                        }
                        if (args.length > 2) {
                            this._triggerChange("" + index, "add", args.slice(2), removed);
                        }
                        can.Observe.stopBatch();
                        return removed;
                    },

                    _attrs: function(items, remove) {
                        if (items === undefined) {
                            return serialize(this, 'attr', []);
                        }

                        // Create a copy.
                        items = can.makeArray(items);

                        Observe.startBatch();
                        this._updateAttrs(items, remove);
                        Observe.stopBatch()
                    },

                    _updateAttrs: function(items, remove) {
                        var len = Math.min(items.length, this.length);

                        for (var prop = 0; prop < len; prop++) {
                            var curVal = this[prop],
                                newVal = items[prop];

                            if (canMakeObserve(curVal) && canMakeObserve(newVal)) {
                                curVal.attr(newVal, remove)
                            } else if (curVal != newVal) {
                                this._set(prop, newVal)
                            } else {

                            }
                        }
                        if (items.length > this.length) {
                            // Add in the remaining props.
                            this.push.apply(this, items.slice(this.length));
                        } else if (items.length < this.length && remove) {
                            this.splice(items.length)
                        }
                    }
                }),

            // Converts to an `array` of arguments.
            getArgs = function(args) {
                return args[0] && can.isArray(args[0]) ?
                    args[0] :
                    can.makeArray(args);
            };
        // Create `push`, `pop`, `shift`, and `unshift`
        can.each({

                push: "length",

                unshift: 0
            },
            // Adds a method
            // `name` - The method name.
            // `where` - Where items in the `array` should be added.

            function(where, name) {
                var orig = [][name]
                list.prototype[name] = function() {
                    // Get the items being added.
                    var args = [],
                        // Where we are going to add items.
                        len = where ? this.length : 0,
                        i = arguments.length,
                        res,
                        val,
                        constructor = this.constructor;

                    // Go through and convert anything to an `observe` that needs to be converted.
                    while (i--) {
                        val = arguments[i];
                        args[i] = canMakeObserve(val) ?
                            hookupBubble(val, "*", this, this.constructor.Observe, this.constructor) :
                            val;
                    }

                    // Call the original method.
                    res = orig.apply(this, args);

                    if (!this.comparator || args.length) {

                        this._triggerChange("" + len, "add", args, undefined);
                    }

                    return res;
                }
            });

        can.each({

                pop: "length",

                shift: 0
            },
            // Creates a `remove` type method

            function(where, name) {
                list.prototype[name] = function() {

                    var args = getArgs(arguments),
                        len = where && this.length ? this.length - 1 : 0;

                    var res = [][name].apply(this, args)

                    // Create a change where the args are
                    // `len` - Where these items were removed.
                    // `remove` - Items removed.
                    // `undefined` - The new values (there are none).
                    // `res` - The old, removed values (should these be unbound).
                    this._triggerChange("" + len, "remove", undefined, [res])

                    if (res && res.unbind) {
                        res.unbind("change" + this._cid)
                    }
                    return res;
                }
            });

        can.extend(list.prototype, {

                indexOf: function(item) {
                    this.attr('length')
                    return can.inArray(item, this)
                },


                join: [].join,


                reverse: [].reverse,


                slice: function() {
                    var temp = Array.prototype.slice.apply(this, arguments);
                    return new this.constructor(temp);
                },


                concat: function() {
                    var args = [];
                    can.each(can.makeArray(arguments), function(arg, i) {
                        args[i] = arg instanceof can.Observe.List ? arg.serialize() : arg;
                    });
                    return new this.constructor(Array.prototype.concat.apply(this.serialize(), args));
                },


                forEach: function(cb, thisarg) {
                    can.each(this, cb, thisarg || this);
                },


                replace: function(newList) {
                    if (can.isDeferred(newList)) {
                        newList.then(can.proxy(this.replace, this));
                    } else {
                        this.splice.apply(this, [0, this.length].concat(can.makeArray(newList || [])));
                    }

                    return this;
                }
            });

        can.List = Observe.List = list;
        Observe.setup = function() {
            can.Construct.setup.apply(this, arguments);
            // I would prefer not to do it this way. It should
            // be using the attributes plugin to do this type of conversion.
            this.List = Observe.List({
                    Observe: this
                }, {});
        }
        return Observe;
    })(__m3, __m8, __m1);

    // ## can/control/control.js
    var __m9 = (function(can) {
        // ## control.js
        // `can.Control`  
        // _Controller_

        // Binds an element, returns a function that unbinds.
        var bind = function(el, ev, callback) {

            can.bind.call(el, ev, callback);

            return function() {
                can.unbind.call(el, ev, callback);
            };
        },
            isFunction = can.isFunction,
            extend = can.extend,
            each = can.each,
            slice = [].slice,
            paramReplacer = /\{([^\}]+)\}/g,
            special = can.getObject("$.event.special", [can]) || {},

            // Binds an element, returns a function that unbinds.
            delegate = function(el, selector, ev, callback) {
                can.delegate.call(el, selector, ev, callback);
                return function() {
                    can.undelegate.call(el, selector, ev, callback);
                };
            },

            // Calls bind or unbind depending if there is a selector.
            binder = function(el, ev, callback, selector) {
                return selector ?
                    delegate(el, can.trim(selector), ev, callback) :
                    bind(el, ev, callback);
            },

            basicProcessor;

        var Control = can.Control = can.Construct(

            {
                // Setup pre-processes which methods are event listeners.

                setup: function() {

                    // Allow contollers to inherit "defaults" from super-classes as it 
                    // done in `can.Construct`
                    can.Construct.setup.apply(this, arguments);

                    // If you didn't provide a name, or are `control`, don't do anything.
                    if (can.Control) {

                        // Cache the underscored names.
                        var control = this,
                            funcName;

                        // Calculate and cache actions.
                        control.actions = {};
                        for (funcName in control.prototype) {
                            if (control._isAction(funcName)) {
                                control.actions[funcName] = control._action(funcName);
                            }
                        }
                    }
                },

                // Moves `this` to the first argument, wraps it with `jQuery` if it's an element
                _shifter: function(context, name) {

                    var method = typeof name == "string" ? context[name] : name;

                    if (!isFunction(method)) {
                        method = context[method];
                    }

                    return function() {
                        context.called = name;
                        return method.apply(context, [this.nodeName ? can.$(this) : this].concat(slice.call(arguments, 0)));
                    };
                },

                // Return `true` if is an action.

                _isAction: function(methodName) {

                    var val = this.prototype[methodName],
                        type = typeof val;
                    // if not the constructor
                    return (methodName !== 'constructor') &&
                    // and is a function or links to a function
                    (type == "function" || (type == "string" && isFunction(this.prototype[val]))) &&
                    // and is in special, a processor, or has a funny character
                    !! (special[methodName] || processors[methodName] || /[^\w]/.test(methodName));
                },
                // Takes a method name and the options passed to a control
                // and tries to return the data necessary to pass to a processor
                // (something that binds things).

                _action: function(methodName, options) {

                    // If we don't have options (a `control` instance), we'll run this 
                    // later.  
                    paramReplacer.lastIndex = 0;
                    if (options || !paramReplacer.test(methodName)) {
                        // If we have options, run sub to replace templates `{}` with a
                        // value from the options or the window
                        var convertedName = options ? can.sub(methodName, [options, window]) : methodName;
                        if (!convertedName) {
                            return null;
                        }
                        // If a `{}` template resolves to an object, `convertedName` will be
                        // an array
                        var arr = can.isArray(convertedName),

                            // Get the name
                            name = arr ? convertedName[1] : convertedName,

                            // Grab the event off the end
                            parts = name.split(/\s+/g),
                            event = parts.pop();

                        return {
                            processor: processors[event] || basicProcessor,
                            parts: [name, parts.join(" "), event],
                            delegate: arr ? convertedName[0] : undefined
                        };
                    }
                },
                // An object of `{eventName : function}` pairs that Control uses to 
                // hook up events auto-magically.

                processors: {},
                // A object of name-value pairs that act as default values for a 
                // control instance
                defaults: {}

            }, {

                // Sets `this.element`, saves the control in `data, binds event
                // handlers.

                setup: function(element, options) {

                    var cls = this.constructor,
                        pluginname = cls.pluginName || cls._fullName,
                        arr;

                    // Want the raw element here.
                    this.element = can.$(element)

                    if (pluginname && pluginname !== 'can_control') {
                        // Set element and `className` on element.
                        this.element.addClass(pluginname);
                    }

                    (arr = can.data(this.element, "controls")) || can.data(this.element, "controls", arr = []);
                    arr.push(this);

                    // Option merging.

                    this.options = extend({}, cls.defaults, options);

                    // Bind all event handlers.
                    this.on();

                    // Gets passed into `init`.

                    return [this.element, this.options];
                },

                on: function(el, selector, eventName, func) {
                    if (!el) {

                        // Adds bindings.
                        this.off();

                        // Go through the cached list of actions and use the processor 
                        // to bind
                        var cls = this.constructor,
                            bindings = this._bindings,
                            actions = cls.actions,
                            element = this.element,
                            destroyCB = can.Control._shifter(this, "destroy"),
                            funcName, ready;

                        for (funcName in actions) {
                            // Only push if we have the action and no option is `undefined`
                            if (actions.hasOwnProperty(funcName) &&
                                (ready = actions[funcName] || cls._action(funcName, this.options))) {
                                bindings.push(ready.processor(ready.delegate || element,
                                        ready.parts[2], ready.parts[1], funcName, this));
                            }
                        }


                        // Setup to be destroyed...  
                        // don't bind because we don't want to remove it.
                        can.bind.call(element, "destroyed", destroyCB);
                        bindings.push(function(el) {
                            can.unbind.call(el, "destroyed", destroyCB);
                        });
                        return bindings.length;
                    }

                    if (typeof el == 'string') {
                        func = eventName;
                        eventName = selector;
                        selector = el;
                        el = this.element;
                    }

                    if (func === undefined) {
                        func = eventName;
                        eventName = selector;
                        selector = null;
                    }

                    if (typeof func == 'string') {
                        func = can.Control._shifter(this, func);
                    }

                    this._bindings.push(binder(el, eventName, func, selector));

                    return this._bindings.length;
                },
                // Unbinds all event handlers on the controller.

                off: function() {
                    var el = this.element[0]
                    each(this._bindings || [], function(value) {
                        value(el);
                    });
                    // Adds bindings.
                    this._bindings = [];
                },
                // Prepares a `control` for garbage collection

                destroy: function() {
                    //Control already destroyed
                    if (this.element === null) {

                        return;
                    }
                    var Class = this.constructor,
                        pluginName = Class.pluginName || Class._fullName,
                        controls;

                    // Unbind bindings.
                    this.off();

                    if (pluginName && pluginName !== 'can_control') {
                        // Remove the `className`.
                        this.element.removeClass(pluginName);
                    }

                    // Remove from `data`.
                    controls = can.data(this.element, "controls");
                    controls.splice(can.inArray(this, controls), 1);

                    can.trigger(this, "destroyed"); // In case we want to know if the `control` is removed.

                    this.element = null;
                }
            });

        var processors = can.Control.processors,
            // Processors do the binding.
            // They return a function that unbinds when called.  
            // The basic processor that binds events.
            basicProcessor = function(el, event, selector, methodName, control) {
                return binder(el, event, can.Control._shifter(control, methodName), selector);
            };

        // Set common events to be processed as a `basicProcessor`
        each(["change", "click", "contextmenu", "dblclick", "keydown", "keyup",
                "keypress", "mousedown", "mousemove", "mouseout", "mouseover",
                "mouseup", "reset", "resize", "scroll", "select", "submit", "focusin",
                "focusout", "mouseenter", "mouseleave",
                // #104 - Add touch events as default processors
                // TOOD feature detect?
                "touchstart", "touchmove", "touchcancel", "touchend", "touchleave"
            ], function(v) {
                processors[v] = basicProcessor;
            });

        return Control;
    })(__m3, __m1);

    // ## can/util/string/deparam/deparam.js
    var __m11 = (function(can) {

        // ## deparam.js  
        // `can.deparam`  
        // _Takes a string of name value pairs and returns a Object literal that represents those params._
        var digitTest = /^\d+$/,
            keyBreaker = /([^\[\]]+)|(\[\])/g,
            paramTest = /([^?#]*)(#.*)?$/,
            prep = function(str) {
                return decodeURIComponent(str.replace(/\+/g, " "));
            };


        can.extend(can, {

                deparam: function(params) {

                    var data = {},
                        pairs, lastPart;

                    if (params && paramTest.test(params)) {

                        pairs = params.split('&'),

                        can.each(pairs, function(pair) {

                            var parts = pair.split('='),
                                key = prep(parts.shift()),
                                value = prep(parts.join("=")),
                                current = data;

                            if (key) {
                                parts = key.match(keyBreaker);

                                for (var j = 0, l = parts.length - 1; j < l; j++) {
                                    if (!current[parts[j]]) {
                                        // If what we are pointing to looks like an `array`
                                        current[parts[j]] = digitTest.test(parts[j + 1]) || parts[j + 1] == "[]" ? [] : {};
                                    }
                                    current = current[parts[j]];
                                }
                                lastPart = parts.pop();
                                if (lastPart == "[]") {
                                    current.push(value);
                                } else {
                                    current[lastPart] = value;
                                }
                            }
                        });
                    }
                    return data;
                }
            });
        return can;
    })(__m3, __m2);

    // ## can/route/route.js
    var __m10 = (function(can) {

        // ## route.js  
        // `can.route`  
        // _Helps manage browser history (and client state) by synchronizing the 
        // `window.location.hash` with a `can.Observe`._  
        // Helper methods used for matching routes.
        var
        // `RegExp` used to match route variables of the type ':name'.
        // Any word character or a period is matched.
        matcher = /\:([\w\.]+)/g,
            // Regular expression for identifying &amp;key=value lists.
            paramsMatcher = /^(?:&[^=]+=[^&]*)+/,
            // Converts a JS Object into a list of parameters that can be 
            // inserted into an html element tag.
            makeProps = function(props) {
                var tags = [];
                can.each(props, function(val, name) {
                    tags.push((name === 'className' ? 'class' : name) + '="' +
                        (name === "href" ? val : can.esc(val)) + '"');
                });
                return tags.join(" ");
            },
            // Checks if a route matches the data provided. If any route variable
            // is not present in the data, the route does not match. If all route
            // variables are present in the data, the number of matches is returned 
            // to allow discerning between general and more specific routes. 
            matchesData = function(route, data) {
                var count = 0,
                    i = 0,
                    defaults = {};
                // look at default values, if they match ...
                for (var name in route.defaults) {
                    if (route.defaults[name] === data[name]) {
                        // mark as matched
                        defaults[name] = 1;
                        count++;
                    }
                }
                for (; i < route.names.length; i++) {
                    if (!data.hasOwnProperty(route.names[i])) {
                        return -1;
                    }
                    if (!defaults[route.names[i]]) {
                        count++;
                    }

                }

                return count;
            },
            onready = !0,
            location = window.location,
            wrapQuote = function(str) {
                return (str + '').replace(/([.?*+\^$\[\]\\(){}|\-])/g, "\\$1");
            },
            each = can.each,
            extend = can.extend;

        can.route = function(url, defaults) {
            defaults = defaults || {};
            // Extract the variable names and replace with `RegExp` that will match
            // an atual URL with values.
            var names = [],
                test = url.replace(matcher, function(whole, name, i) {
                    names.push(name);
                    var next = "\\" + (url.substr(i + whole.length, 1) || can.route._querySeparator);
                    // a name without a default value HAS to have a value
                    // a name that has a default value can be empty
                    // The `\\` is for string-escaping giving single `\` for `RegExp` escaping.
                    return "([^" + next + "]" + (defaults[name] ? "*" : "+") + ")";
                });

            // Add route in a form that can be easily figured out.
            can.route.routes[url] = {
                // A regular expression that will match the route when variable values 
                // are present; i.e. for `:page/:type` the `RegExp` is `/([\w\.]*)/([\w\.]*)/` which
                // will match for any value of `:page` and `:type` (word chars or period).
                test: new RegExp("^" + test + "($|" + wrapQuote(can.route._querySeparator) + ")"),
                // The original URL, same as the index for this entry in routes.
                route: url,
                // An `array` of all the variable names in this route.
                names: names,
                // Default values provided for the variables.
                defaults: defaults,
                // The number of parts in the URL separated by `/`.
                length: url.split('/').length
            };
            return can.route;
        };


        extend(can.route, {

                _querySeparator: '&',
                _paramsMatcher: paramsMatcher,


                param: function(data, _setRoute) {
                    // Check if the provided data keys match the names in any routes;
                    // Get the one with the most matches.
                    var route,
                        // Need to have at least 1 match.
                        matches = 0,
                        matchCount,
                        routeName = data.route,
                        propCount = 0;

                    delete data.route;

                    each(data, function() {
                        propCount++;
                    });
                    // Otherwise find route.
                    each(can.route.routes, function(temp, name) {
                        // best route is the first with all defaults matching


                        matchCount = matchesData(temp, data);
                        if (matchCount > matches) {
                            route = temp;
                            matches = matchCount;
                        }
                        if (matchCount >= propCount) {
                            return false;
                        }
                    });
                    // If we have a route name in our `can.route` data, and it's
                    // just as good as what currently matches, use that
                    if (can.route.routes[routeName] && matchesData(can.route.routes[routeName], data) === matches) {
                        route = can.route.routes[routeName];
                    }
                    // If this is match...
                    if (route) {
                        var cpy = extend({}, data),
                            // Create the url by replacing the var names with the provided data.
                            // If the default value is found an empty string is inserted.
                            res = route.route.replace(matcher, function(whole, name) {
                                delete cpy[name];
                                return data[name] === route.defaults[name] ? "" : encodeURIComponent(data[name]);
                            }),
                            after;
                        // Remove matching default values
                        each(route.defaults, function(val, name) {
                            if (cpy[name] === val) {
                                delete cpy[name];
                            }
                        });

                        // The remaining elements of data are added as 
                        // `&amp;` separated parameters to the url.
                        after = can.param(cpy);
                        // if we are paraming for setting the hash
                        // we also want to make sure the route value is updated
                        if (_setRoute) {
                            can.route.attr('route', route.route);
                        }
                        return res + (after ? can.route._querySeparator + after : "");
                    }
                    // If no route was found, there is no hash URL, only paramters.
                    return can.isEmptyObject(data) ? "" : can.route._querySeparator + can.param(data);
                },

                deparam: function(url) {
                    // See if the url matches any routes by testing it against the `route.test` `RegExp`.
                    // By comparing the URL length the most specialized route that matches is used.
                    var route = {
                        length: -1
                    };
                    each(can.route.routes, function(temp, name) {
                        if (temp.test.test(url) && temp.length > route.length) {
                            route = temp;
                        }
                    });
                    // If a route was matched.
                    if (route.length > -1) {

                        var // Since `RegExp` backreferences are used in `route.test` (parens)
                        // the parts will contain the full matched string and each variable (back-referenced) value.
                        parts = url.match(route.test),
                            // Start will contain the full matched string; parts contain the variable values.
                            start = parts.shift(),
                            // The remainder will be the `&amp;key=value` list at the end of the URL.
                            remainder = url.substr(start.length - (parts[parts.length - 1] === can.route._querySeparator ? 1 : 0)),
                            // If there is a remainder and it contains a `&amp;key=value` list deparam it.
                            obj = (remainder && can.route._paramsMatcher.test(remainder)) ? can.deparam(remainder.slice(1)) : {};

                        // Add the default values for this route.
                        obj = extend(true, {}, route.defaults, obj);
                        // Overwrite each of the default values in `obj` with those in 
                        // parts if that part is not empty.
                        each(parts, function(part, i) {
                            if (part && part !== can.route._querySeparator) {
                                obj[route.names[i]] = decodeURIComponent(part);
                            }
                        });
                        obj.route = route.route;
                        return obj;
                    }
                    // If no route was matched, it is parsed as a `&amp;key=value` list.
                    if (url.charAt(0) !== can.route._querySeparator) {
                        url = can.route._querySeparator + url;
                    }
                    return can.route._paramsMatcher.test(url) ? can.deparam(url.slice(1)) : {};
                },

                data: new can.Observe({}),

                routes: {},

                ready: function(val) {
                    if (val === false) {
                        onready = val;
                    }
                    if (val === true || onready === true) {
                        can.route._setup();
                        setState();
                    }
                    return can.route;
                },

                url: function(options, merge) {
                    if (merge) {
                        options = extend({}, curParams, options)
                    }
                    return "#!" + can.route.param(options);
                },

                link: function(name, options, props, merge) {
                    return "<a " + makeProps(
                        extend({
                                href: can.route.url(options, merge)
                            }, props)) + ">" + name + "</a>";
                },

                current: function(options) {
                    return location.hash == "#!" + can.route.param(options)
                },
                _setup: function() {
                    // If the hash changes, update the `can.route.data`.
                    can.bind.call(window, 'hashchange', setState);
                },
                _getHash: function() {
                    return location.href.split(/#!?/)[1] || "";
                },
                _setHash: function(serialized) {
                    var path = (can.route.param(serialized, true));
                    location.hash = "#!" + path;
                    return path;
                }
            });


        // The functions in the following list applied to `can.route` (e.g. `can.route.attr('...')`) will
        // instead act on the `can.route.data` observe.
        each(['bind', 'unbind', 'delegate', 'undelegate', 'attr', 'removeAttr'], function(name) {
            can.route[name] = function() {
                // `delegate` and `undelegate` require
                // the `can/observe/delegate` plugin
                if (!can.route.data[name]) {
                    return;
                }

                return can.route.data[name].apply(can.route.data, arguments);
            }
        })

        var // A ~~throttled~~ debounced function called multiple times will only fire once the
        // timer runs down. Each call resets the timer.
        timer,
            // Intermediate storage for `can.route.data`.
            curParams,
            // Deparameterizes the portion of the hash of interest and assign the
            // values to the `can.route.data` removing existing values no longer in the hash.
            // setState is called typically by hashchange which fires asynchronously
            // So it's possible that someone started changing the data before the 
            // hashchange event fired.  For this reason, it will not set the route data
            // if the data is changing or the hash already matches the hash that was set.
            setState = can.route.setState = function() {
                var hash = can.route._getHash();
                curParams = can.route.deparam(hash);

                // if the hash data is currently changing, or
                // the hash is what we set it to anyway, do NOT change the hash
                if (!changingData || hash !== lastHash) {
                    can.route.attr(curParams, true);
                }
            },
            // The last hash caused by a data change
            lastHash,
            // Are data changes pending that haven't yet updated the hash
            changingData;

        // If the `can.route.data` changes, update the hash.
        // Using `.serialize()` retrieves the raw data contained in the `observable`.
        // This function is ~~throttled~~ debounced so it only updates once even if multiple values changed.
        // This might be able to use batchNum and avoid this.
        can.route.bind("change", function(ev, attr) {
            // indicate that data is changing
            changingData = 1;
            clearTimeout(timer);
            timer = setTimeout(function() {
                // indicate that the hash is set to look like the data
                changingData = 0;
                var serialized = can.route.data.serialize();

                lastHash = can.route._setHash(serialized);
            }, 1);
        });
        // `onready` event...
        can.bind.call(document, "ready", can.route.ready);

        // Libraries other than jQuery don't execute the document `ready` listener
        // if we are already DOM ready
        if ((document.readyState === 'complete' || document.readyState === "interactive") && onready) {
            can.route.ready();
        }

        // extend route to have a similar property 
        // that is often checked in mustache to determine
        // an object's observability
        can.route.constructor.canMakeObserve = can.Observe.canMakeObserve;

        return can.route;
    })(__m3, __m7, __m11);

    // ## can/construct/super/super.js
    var __m12 = (function(can, Construct) {

        // tests if we can get super in .toString()
        var isFunction = can.isFunction,

            fnTest = /xyz/.test(function() {
                xyz;
            }) ? /\b_super\b/ : /.*/;

        // overwrites a single property so it can still call super
        can.Construct._overwrite = function(addTo, base, name, val) {
            // Check if we're overwriting an existing function
            addTo[name] = isFunction(val) &&
                isFunction(base[name]) &&
                fnTest.test(val) ? (function(name, fn) {
                    return function() {
                        var tmp = this._super,
                            ret;

                        // Add a new ._super() method that is the same method
                        // but on the super-class
                        this._super = base[name];

                        // The method only need to be bound temporarily, so we
                        // remove it when we're done executing
                        ret = fn.apply(this, arguments);
                        this._super = tmp;
                        return ret;
                    };
                })(name, val) : val;
        }

        // overwrites an object with methods, sets up _super
        //   newProps - new properties
        //   oldProps - where the old properties might be
        //   addTo - what we are adding to
        can.Construct._inherit = function(newProps, oldProps, addTo) {
            addTo = addTo || newProps
            for (var name in newProps) {
                can.Construct._overwrite(addTo, oldProps, name, newProps[name]);
            }
        }

        return can;
    })(__m3, __m1);

    // ## can/construct/proxy/proxy.js
    var __m13 = (function(can, Construct) {
        var isFunction = can.isFunction,
            isArray = can.isArray,
            makeArray = can.makeArray,

            proxy = function(funcs) {

                //args that should be curried
                var args = makeArray(arguments),
                    self;

                // get the functions to callback
                funcs = args.shift();

                // if there is only one function, make funcs into an array
                if (!isArray(funcs)) {
                    funcs = [funcs];
                }

                // keep a reference to us in self
                self = this;


                return function class_cb() {
                    // add the arguments after the curried args
                    var cur = args.concat(makeArray(arguments)),
                        isString,
                        length = funcs.length,
                        f = 0,
                        func;

                    // go through each function to call back
                    for (; f < length; f++) {
                        func = funcs[f];
                        if (!func) {
                            continue;
                        }

                        // set called with the name of the function on self (this is how this.view works)
                        isString = typeof func == "string";

                        // call the function
                        cur = (isString ? self[func] : func).apply(self, cur || []);

                        // pass the result to the next function (if there is a next function)
                        if (f < length - 1) {
                            cur = !isArray(cur) || cur._use_call ? [cur] : cur
                        }
                    }
                    return cur;
                }
            }
        can.Construct.proxy = can.Construct.prototype.proxy = proxy;
        // this corrects the case where can/control loads after can/construct/proxy, so static props don't have proxy
        var correctedClasses = [can.Observe, can.Control, can.Model],
            i = 0;
        for (; i < correctedClasses.length; i++) {
            if (correctedClasses[i]) {
                correctedClasses[i].proxy = proxy;
            }
        }
        return can;
    })(__m3, __m1);

    // ## can/control/plugin/plugin.js
    var __m14 = (function($, can) {
        //used to determine if a control instance is one of controllers
        //controllers can be strings or classes
        var i,
            isAControllerOf = function(instance, controllers) {
                for (i = 0; i < controllers.length; i++) {
                    if (typeof controllers[i] == 'string' ? instance.constructor._shortName == controllers[i] : instance instanceof controllers[i]) {
                        return true;
                    }
                }
                return false;
            },
            makeArray = can.makeArray,
            old = can.Control.setup;

        can.Control.setup = function() {
            // if you didn't provide a name, or are control, don't do anything
            if (this !== can.Control) {


                var pluginName = this.pluginName || this._fullName;

                // create jQuery plugin
                if (pluginName !== 'can_control') {
                    this.plugin(pluginName);
                }

                old.apply(this, arguments);
            }
        };

        $.fn.extend({


                controls: function() {
                    var controllerNames = makeArray(arguments),
                        instances = [],
                        controls, c, cname;
                    //check if arguments
                    this.each(function() {

                        controls = can.$(this).data("controls");
                        if (!controls) {
                            return;
                        }
                        for (var i = 0; i < controls.length; i++) {
                            c = controls[i];
                            if (!controllerNames.length || isAControllerOf(c, controllerNames)) {
                                instances.push(c);
                            }
                        }
                    });
                    return instances;
                },


                control: function(control) {
                    return this.controls.apply(this, arguments)[0];
                }
            });

        can.Control.plugin = function(pluginname) {
            var control = this;

            if (!$.fn[pluginname]) {
                $.fn[pluginname] = function(options) {

                    var args = makeArray(arguments), //if the arg is a method on this control
                        isMethod = typeof options == "string" && $.isFunction(control.prototype[options]),
                        meth = args[0],
                        returns;
                    this.each(function() {
                        //check if created
                        var plugin = can.$(this).control(control);

                        if (plugin) {
                            if (isMethod) {
                                // call a method on the control with the remaining args
                                returns = plugin[meth].apply(plugin, args.slice(1));
                            } else {
                                // call the plugin's update method
                                plugin.update.apply(plugin, args);
                            }
                        } else {
                            //create a new control instance
                            control.newInstance.apply(control, [this].concat(args));
                        }
                    });
                    return returns !== undefined ? returns : this;
                };
            }
        }

        can.Control.prototype.update = function(options) {
            can.extend(this.options, options);
            this.on();
        };

        return can;
    })(jQuery, __m3, __m9);

    window['can'] = __m5;
})();