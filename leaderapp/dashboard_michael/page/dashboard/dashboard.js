frappe.pages["dashboard"].on_page_load = function (wrapper) {
	frappe.dashboard = new frappe.Dashboard(wrapper);
}

frappe.Dashboard = Class.extend({

	init: function (parent) {
		frappe.ui.make_app_page({
			parent: parent,
			title: "Dashboard",
			single_column: false
		});

		this.parent = parent;
		this.page = this.parent.page;
		this.page.sidebar.html(`<ul class="module-sidebar-nav overlay-sidebar nav nav-pills nav-stacked"></ul>`);
		this.$sidebar_list = this.page.sidebar.find('ul');

		// const list of doctypes
		this.doctypes = ["Sales Order"];
		this.timespans = ["Week", "Month", "Quarter", "Year"];
		this.filters = {
			"Sales Order": ["grand_total", "base_grand_total"],
		};

		// for saving current selected filters
//		 TODO: revert to 0 index for doctype and timespan, and remove preset down
		const _initial_doctype = this.doctypes[0];
		const _initial_timespan = this.timespans[0];
		const _initial_filter = this.filters[_initial_doctype];

		this.options = {
			selected_doctype: _initial_doctype,
			selected_filter: _initial_filter,
			selected_filter_item: _initial_filter[0],
			selected_timespan: _initial_timespan,
		};

		this.message = null;
		this.make();
	},

	make: function () {
		var me = this;

		var $container = $(`<div class="dashboard page-main-content">
			<div class="dashboard-graph" style="width: 50%; float: left;"></div>
			<div class="dashboard-graph2" style="width: 50%; float: right;"></div>
			<div class="dashboard-graph3" style="width: 100%; float: right;"></div>
		</div>`).appendTo(this.page.main);

		this.$graph_area = $container.find('.dashboard-graph');
		this.$graph_area2 = $container.find('.dashboard-graph2');
		this.$graph_area3 = $container.find('.dashboard-graph3');

		this.doctypes.map(doctype => {
			this.get_sidebar_item(doctype).appendTo(this.$sidebar_list);
		});

		this.company_select = this.page.add_field({
			fieldname: 'company',
			label: __('Company'),
			fieldtype:'Link',
			options:'Company',
			default:frappe.defaults.get_default('company'),
			reqd: 1,
			change: function() {
				me.options.selected_company = this.value;
				me.make_request($container);
			}
		});
		this.timespan_select = this.page.add_select(__("Timespan"),
			this.timespans.map(d => {
				return {"label": __(d), value: d }
			})
		);

		this.type_select = this.page.add_select(__("Type"),
			me.options.selected_filter.map(d => {
				return {"label": __(frappe.model.unscrub(d)), value: d }
			})
		);

		this.$sidebar_list.on('click', 'li', function(e) {
			let $li = $(this);
			let doctype = $li.find('span').html();

			me.options.selected_company = frappe.defaults.get_default('company');
			me.options.selected_doctype = doctype;
			me.options.selected_filter = me.filters[doctype];
			me.options.selected_filter_item = me.filters[doctype][0];

			me.type_select.empty().add_options(
				me.options.selected_filter.map(d => {
					return {"label": __(frappe.model.unscrub(d)), value: d }
				})
			);

			me.$sidebar_list.find('li').removeClass('active');
			$li.addClass('active');

			me.make_request($container);
		});

		this.timespan_select.on("change", function() {
			me.options.selected_timespan = this.value;
			me.make_request($container);
		});

		this.type_select.on("change", function() {
			me.options.selected_filter_item = this.value
			me.make_request($container);
		});

		// now get dashboard
		this.$sidebar_list.find('li:first').trigger('click');
	},

	make_request: function ($container) {
		var me = this;

		frappe.model.with_doctype(me.options.selected_doctype, function () {
			me.get_dashboard(me.get_dashboard_data, $container);
			me.get_dashboard2(me.get_dashboard_data, $container);
			me.get_dashboard3(me.get_dashboard_data, $container);
		});
	},

	get_dashboard: function (notify, $container) {
		var me = this;
		if(!me.options.selected_company) {
			frappe.throw(__("Please select Company"));
		}
		frappe.call({
			method: "leaderapp.dashboard_michael.page.dashboard.dashboard.get_dashboard",
			args: {
				doctype: me.options.selected_doctype,
				timespan: me.options.selected_timespan,
				company: me.options.selected_company,
				field: me.options.selected_filter_item,
			},
			callback: function (r) {
				let results = r.message || [];

				let graph_items = results.slice(0, 10);

				me.$graph_area.show().empty();
				let args = {
					parent: '.dashboard-graph',
					data: {
						datasets: [
							{
								values: graph_items.map(d=>d.value)
							}
						],
						labels: graph_items.map(d=>d.name)
					},
					colors: ['light-green'],
					format_tooltip_x: d=>d[me.options.selected_filter_item],
					type: 'bar',
					height: 140
				};
				var chart1 = new Chart(args);

				notify(me, r, $container);
			}
		});
	},

	get_dashboard2: function (notify, $container) {
		var me = this;
		if(!me.options.selected_company) {
			frappe.throw(__("Please select Company"));
		}
		frappe.call({
			method: "leaderapp.dashboard_michael.page.dashboard.dashboard.get_dashboard2",
			args: {
				doctype: me.options.selected_doctype,
				timespan: me.options.selected_timespan,
				company: me.options.selected_company,
				field: me.options.selected_filter_item,
			},
			callback: function (r) {
				let results = r.message || [];

				let graph_items = results.slice(0, 10);

				me.$graph_area2.show().empty();
				let args = {
					parent: '.dashboard-graph2',
					data: {
						datasets: [
							{
								values: graph_items.map(d=>d.value)
							}
						],
						labels: graph_items.map(d=>d.name)
					},
					colors: ['light-green'],
					format_tooltip_x: d=>d[me.options.selected_filter_item],
					type: 'line',
					height: 140
				};
				var chart2 = new Chart(args);

				notify(me, r, $container);
			}
		});
	},

	get_dashboard3: function (notify, $container) {
		var me = this;
		if(!me.options.selected_company) {
			frappe.throw(__("Please select Company"));
		}
		frappe.call({
			method: "leaderapp.dashboard_michael.page.dashboard.dashboard.get_dashboard3",
			args: {
				doctype: me.options.selected_doctype,
				timespan: me.options.selected_timespan,
				company: me.options.selected_company,
				field: me.options.selected_filter_item,
			},
			callback: function (r) {
				let results = r.message || [];

				let graph_items = results.slice(0, 10);

				me.$graph_area3.show().empty();
				let args = {
					parent: '.dashboard-graph3',
					data: {
						datasets: [
							{
								values: graph_items.map(d=>d.value)
							}
						],
						labels: graph_items.map(d=>d.name)
					},
					colors: ['light-green'],
					format_tooltip_x: d=>d[me.options.selected_filter_item],
					type: 'line',
					height: 140
				};
				var chart3 = new Chart(args);

				notify(me, r, $container);
			}
		});
	},

	get_sidebar_item: function(item) {
		return $(`<li class="strong module-sidebar-item">
			<a class="module-link">
			<span>${ item }</span></a>
		</li>`);
	}
});
