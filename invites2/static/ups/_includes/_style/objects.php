<div class="style-container objects style-pane">
<ul>

<li class="style-node style-node-btn">
	<label class="style-node-h">Button - Default</label>
	<div class="style-example">
	<a href="#" class="btn-small">Small Button</a>
	<a href="#" class="btn">Regular Button</a>
	<a href="#" class="btn-large">Large Button</a>
	</div> <!-- style example -->
	<div class="style-meta-container">
		<dl class="style-meta">
			<dt>Selector</dt>
			<dd>.btn</dd>
			<?php echo $code_snip ?>
		</dl> 
	</div> <!-- style-meta -->	
</li>

<li class="style-node style-node-btn">
	<label class="style-node-h">Button - Light</label>
	<div class="style-example">
	<a href="#" class="btn-small-light">Small Light</a>
	<a href="#" class="btn-light">Regular Light</a>
	<a href="#" class="btn-large-light">Large Light</a>
	</div> <!-- style example -->
	<div class="style-meta-container">
		<dl class="style-meta">
			<dt>Selector</dt>
			<dd>.btn-light</dd>
			<?php echo $code_snip ?>
		</dl> 
	</div> <!-- style-meta -->	
</li>

<li class="style-node style-node-btn">
	<label class="style-node-h">Button - Dark</label>
	<div class="style-example">
	<a href="#" class="btn-small-dark">Small Dark</a>
	<a href="#" class="btn-dark">Regular Dark</a>
	<a href="#" class="btn-large-dark">Large Dark</a>
	</div> <!-- style example -->
	<div class="style-meta-container">
		<dl class="style-meta">
			<dt>Selector</dt>
			<dd>.btn-dark</dd>
			<?php echo $code_snip ?>
		</dl> 
	</div> <!-- style-meta -->	
</li>

<li class="style-node style-node-btn">
	<label class="style-node-h">Button - Alt</label>
	<div class="style-example">
	<a href="#" class="btn-small-alt">Small Alt</a>
	<a href="#" class="btn-alt">Regular Alt</a>
	<a href="#" class="btn-large-alt">Large Alt</a>
	</div> <!-- style example -->
	<div class="style-meta-container">
		<dl class="style-meta">
			<dt>Selector</dt>
			<dd>.btn-alt</dd>
			<?php echo $code_snip ?>
		</dl> 
	</div> <!-- style-meta -->	
</li>

<li class="style-node">
	<label class="style-node-h">Tabs</label>
	<div class="style-example">
		<ul class="tabs large">
			<li><a href="tab1">Tab 1</a></li>
			<li><a href="tab2">Tab 2</a></li>
			<li><a href="tab3">Tab 3</a></li>
		</ul>
		<div class="tab1 pane">Pane 1</div>
		<div class="tab2 pane">Pane 2</div>
		<div class="tab3 pane">Pane 3</div>
	</div> <!-- style example -->
	<div class="style-meta-container">
		<dl class="style-meta">
			<?php echo $code_snip ?>
		</dl> 
	</div> <!-- style-meta -->	
</li>

<li class="style-node">
	<label class="style-node-h">Pills</label>
	<div class="style-example">
		<ul class="pills large">
			<li><a href="pill1">Pill 1</a></li>
			<li><a href="pill2">Pill 2</a></li>
			<li><a href="pill3">Pill 3</a></li>
		</ul>
		<div class="pill1 pane">Pane 1</div>
		<div class="pill2 pane">Pane 2</div>
		<div class="pill3 pane">Pane 3</div>
	</div> <!-- style example -->
	<div class="style-meta-container">
		<dl class="style-meta">
			<?php echo $code_snip ?>
		</dl> 
	</div> <!-- style-meta -->	
</li>

<li class="style-node">
	<label class="style-node-h">Dropdown - On Hover</label>
	<div class="style-example">
		<div class="dropdown">								 
			<div class="dropdown-trigger-hover">
				<a class="dropdown-trigger-link">Dropdown Hover</a>
				<ul class="dropdown-menu">
					<li><a href="#">Drop Item 1</a></li>
					<li><a href="#">Drop Item 2</a></li>
					<li><a href="#">Drop Item 3</a></li>
					<li><a href="#">Drop Item 4</a></li>
					<li><a href="#">Drop Item 5</a></li>
					<li><a href="#">Drop Item 6</a></li>
					<li><a href="#">Drop Item 7</a></li>
				</ul> <!-- /.dropdown-menu -->
			</div> <!-- /.dropdown-trigger-hover -->			
		</div> <!-- /.dropdown-container -->
	</div> <!-- style example -->
	<div class="style-meta-container">
		<dl class="style-meta">
			<dt>Note</dt>
			<dd>Use "dropdown-trigger-hover" on the containing div</dd>
			<?php echo $code_snip ?>
		</dl> 
	</div> <!-- style-meta -->	
</li>

<li class="style-node">
	<label class="style-node-h">Dropdown - On Click</label>
	<div class="style-example">
		<div class="dropdown">								 
			<a class="dropdown-trigger">Dropdown Click</a>
			<ul class="dropdown-menu">
				<li><a href="#">Drop Item 1</a></li>
				<li><a href="#">Drop Item 2</a></li>
				<li><a href="#">Drop Item 3</a></li>
				<li><a href="#">Drop Item 4</a></li>
				<li><a href="#">Drop Item 5</a></li>
				<li><a href="#">Drop Item 6</a></li>
				<li><a href="#">Drop Item 7</a></li>
			</ul> <!-- /.dropdown-menu -->			
		</div> <!-- /.dropdown-container -->
	</div> <!-- style example -->
	<div class="style-meta-container">
		<dl class="style-meta">
			<dt>Note</dt>
			<dd>Use "dropdown-trigger" on the containing div</dd>
			<?php echo $code_snip ?>
		</dl> 
	</div> <!-- style-meta -->	
</li>

<li class="style-node">
	<label class="style-node-h">Tooltips</label>
	<div class="style-meta-container">
		<dl class="style-meta">
			<dt>Note</dt>
			<dd>For small pieces of helper text, shown on hover. Can be used for any element. Text shown here for demonstration purposes only.</dd>
			<?php echo $code_snip ?>
		</dl> 
	</div> <!-- style-meta -->
	<div class="style-example">
	<article class="text">
		<a class="tip-trigger" href="#">Tooltip example <div class="tooltip">Tooltip text here</div></a>. Sample text shown here. Sample text shown here. Sample text shown here. Sample text shown here. Sample text shown here. Sample text shown here. Sample text shown here. Sample text shown here. 
	</article> <!-- /.text -->
	</div></li>

<li class="style-node">
	<label class="style-node-h">Popovers</label>
	<div class="style-meta-container">
		<dl class="style-meta">
			<dt>Note</dt>
			<dd>For larger pieces of helper text, shown on hover. Can be used for any element. Text shown here for demonstration purposes only.</dd>
			<?php echo $code_snip ?>
		</dl> 
	</div> <!-- style-meta -->
	<div class="style-example">
	<article class="text-large">
		<a class="pop-trigger" href="#">Popover example <div class="popover">Popover text here. Popovers should be used for larger pieces of text and might include images, links, etc. Think about the big popovers on Netflix.</div></a>. Sample text shown here. Sample text shown here. Sample text shown here. Sample text shown here. Sample text shown here. Sample text shown here. Sample text shown here. Sample text shown here. 
	</article> <!-- /.text -->
	</div></li>

<li class="style-node">
	<label class="style-node-h">Modals</label>
	<div class="style-meta-container">
		<dl class="style-meta">
			<dt>Note</dt>
			<dd>Interstitial screens for messages, alerts, forms, etc.</dd>
			<?php echo $code_snip ?>
		</dl> 
	</div> <!-- style-meta -->
	<div class="style-example">
		<a class="modal-trigger btn">Click to Launch Modal</a> 
		<section class="modal">
			<div class="modal-content">
				<p class="txt-l">This is an example of a modal container with content inside. Click anywhere outside the modal to dismiss. Or hit ESC. Or make yourself a close button.</p>
			</div> <!-- /.modal-content -->
		</section> <!-- /.modal -->
	</div></li>

</ul>
</div> <!-- style-container -->
