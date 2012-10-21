<div class="style-container objects style-pane">
	<ul>

		<li class="style-node">
			<label class="style-node-h">Input Box - Small</label>
			<div class="style-meta-container">
				<dl class="style-meta">
					<dt>Note</dt>
					<dd>By default, form labels stack on top of inputs. Styles are set by a class on the parent container, either the entire form or a div surrounding the form field</dd>
					<dt>Selector</dt>
					<dd>.form-s, .form-small</dd>
					<?php echo $code_snip ?>
				</dl>
			</div> <!-- style-meta -->	
			<div class="style-example">
				<form class="form-small">
					<div class="form-row">
						<label for="standard-input">Small Label</label>
						<div class="input">
							<input class="span-30" type="text" id="standard-input" name="standard-input"
								placeholder="Small text input field" />
						</div> <!-- /.input -->
					</div> <!-- /.form-row -->	
				</form> <!-- /.form-large -->	
			</div> <!-- style example --> 
		</li>

		<li class="style-node">
			<label class="style-node-h">Input Box - Default</label>
			<div class="style-meta-container">
				<dl class="style-meta">
					<dt>Note</dt>
					<dd>Vary the width of the input by adding a class of "span-x" (x is a percentage in multiples of 5). Widths may also be added in the CSS instead of using presentational classes.</dd>
					<dt>Selector</dt>
					<dd>.form, .form-m, .form-med</dd>
					<?php echo $code_snip ?>
				</dl>
			</div> <!-- style-meta -->	
			<div class="style-example">
				<form class="form">
					<div class="form-row">
						<label for="standard-input">Default Label</label>
						<div class="input">
							<input  class="span-50" type="text" id="standard-input" name="standard-input"
								placeholder="Standard text input field" />
						</div> <!-- /.input -->
					</div> <!-- /.form-row -->	
				</form> <!-- /.form-large -->	
			</div> <!-- style example --> 
		</li>

		<li class="style-node">
			<label class="style-node-h">Input Box - Large</label>
			<div class="style-meta-container">
				<dl class="style-meta">
					<dt>Selector</dt>
					<dd>.form-l, .form-large</dd>
					<?php echo $code_snip ?>
				</dl>
			</div> <!-- style-meta -->	
			<div class="style-example">
				<form class="form-large">
					<div class="form-row">
						<label for="standard-input">Large Label</label>
						<div class="input">
							<input  class="span-70" type="text" id="standard-input" name="standard-input"
								placeholder="Large text input field" />
						</div> <!-- /.input -->
					</div> <!-- /.form-row -->	
				</form> <!-- /.form-large -->	
			</div> <!-- style example --> 
		</li>

		<li class="style-node">
			<label class="style-node-h">Sidesaddle Label - Small</label>
			<div class="style-meta-container">
				<dl class="style-meta">
					<dt>Note</dt>
					<dd>Just add a class of "sidesaddle" to any type of form</dd>
					<dt>Selector</dt>
					<dd>.sidesaddle</dd>
					<?php echo $code_snip ?>
				</dl>
			</div> <!-- style-meta -->	
			<div class="style-example">
				<form class="form-small sidesaddle" action="#" method="post">
					<div class="form-row">
						<label for="standard-input">Sidesaddle Label</label>
						<div class="input">
							<input  class="span-50" type="text" name="standard-input"
								placeholder="Standard text input field" />
						</div> <!-- /.input -->		
					</div> <!-- /.form-row -->
				</form> <!-- /.form -->
			</div> <!-- style example --> 
		</li>

		<li class="style-node">
			<label class="style-node-h">Sidesaddle Label</label>
			<div class="style-meta-container">
				<dl class="style-meta">
					<dt>Note</dt>
					<dd>Just add a class of "sidesaddle" to any type of form</dd>
					<dt>Selector</dt>
					<dd>.sidesaddle</dd>
					<?php echo $code_snip ?>
				</dl>
			</div> <!-- style-meta -->	
			<div class="style-example">
				<form class="form sidesaddle" action="#" method="post">
					<div class="form-row">
						<label for="standard-input">Sidesaddle Label</label>
						<div class="input">
							<input  class="span-50" type="text" name="standard-input"
								placeholder="Standard text input field" />
						</div> <!-- /.input -->		
					</div> <!-- /.form-row -->
				</form> <!-- /.form -->
			</div> <!-- style example --> 
		</li>

		<li class="style-node">
			<label class="style-node-h">Sidesaddle Label - Large</label>
			<div class="style-meta-container">
				<dl class="style-meta">
					<dt>Note</dt>
					<dd>Just add a class of "sidesaddle" to any type of form</dd>
					<dt>Selector</dt>
					<dd>.sidesaddle</dd>
					<?php echo $code_snip ?>
				</dl>
			</div> <!-- style-meta -->	
			<div class="style-example">
				<form class="form-large sidesaddle" action="#" method="post">
					<div class="form-row">
						<label for="standard-input">Sidesaddle Label</label>
						<div class="input">
							<input  class="span-50" type="text" name="standard-input"
								placeholder="Standard text input field" />
						</div> <!-- /.input -->		
					</div> <!-- /.form-row -->
				</form> <!-- /.form -->
			</div> <!-- style example --> 
		</li>

		<li class="style-node">
			<label class="style-node-h">Text Input with Search Button</label>
			<div class="style-meta-container">
				<dl class="style-meta">
					<dt>Note</dt>
					<dd>Styles are set by a class on the parent container, either the entire form or the div surrounding the form field</dd>
					<?php echo $code_snip ?>
				</dl>
			</div> <!-- style-meta -->	
			<div class="style-example">
				<form class="form">
					<div class="form-row">
						<div class="input">
							<input id="search-input" type="text"
								placeholder="Search thousands of public documents" />
							<input class="btn" type="submit" 
								value="Search">
						</div> <!-- /.input -->
					</div> <!-- /.form-row -->
				</form> <!-- /.form -->
			</div> <!-- style example --> 
		</li>

		<li class="style-node">
			<label class="style-node-h">Legend / Form Header</label>
			<div class="style-meta-container">
				<dl class="style-meta">
					<dt>Selector</dt>
					<dd>.legend-h</dd>
					<?php echo $code_snip ?>
				</dl>
			</div> <!-- style-meta -->	
			<div class="style-example">
	        	<h1 class="legend-h">Example form legend</h1>
			</div> <!-- style example --> 
		</li>

		<li class="style-node">
			<label class="style-node-h">Textarea</label>
			<div class="style-meta-container">
				<dl class="style-meta">
					<?php echo $code_snip ?>
				</dl>
			</div> <!-- style-meta -->	
			<div class="style-example">
				<form class="form">
					<div class="form-row">
			            <label for="textarea">Textarea</label>
			            <div class="input">
			              <textarea  id="textarea2" name="textarea2" rows="3"></textarea>
						</div> <!-- /.input -->
					</div> <!-- /.form-row -->
				</form> <!-- /.form -->
			</div> <!-- style example --> 
		</li>

		<li class="style-node">
			<label class="style-node-h">Select Menu</label>
			<div class="style-meta-container">
				<dl class="style-meta">
					<dt>Note</dt>
					<dd>Simply replace the background images to customize this (webkit and mozilla only)</dd>
					<?php echo $code_snip ?>
				</dl>
			</div> <!-- style-meta -->	
			<div class="style-example">
				<form class="form">
					<div class="form-row">
						<label for="normalSelect">Select</label>
						<div class="input">
							<select name="normalSelect" id="normalSelect">
								<option>1</option>
								<option>2</option>
								<option>3</option>
								<option>4</option>
								<option>5</option>
							</select> <!-- /.select -->
						</div> <!-- /.input -->
					</div> <!-- /.form-row -->
				</form> <!-- /.form -->
			</div> <!-- style example --> 
		</li>

		<li class="style-node">
			<label class="style-node-h">Multiple Select</label>
			<div class="style-meta-container">
				<dl class="style-meta">
					<?php echo $code_snip ?>
				</dl>
			</div> <!-- style-meta -->	
			<div class="style-example">
				<form class="form">
					<div class="form-row">
						<label for="multiSelect">Multiple Select</label>
						<div class="input">
			              <select size="5" multiple="multiple" name="multiSelect" id="multiSelect">
			                <option>1</option>
			                <option>2</option>
			                <option>3</option>
			                <option>4</option>
			                <option>5</option>
			              </select>
						</div> <!-- /.input -->
					</div> <!-- /.form-row -->
				</form> <!-- /.form -->
			</div> <!-- style example --> 
		</li>
	
		<li class="style-node">
			<label class="style-node-h">File Input</label>
			<div class="style-meta-container">
				<dl class="style-meta">
					<?php echo $code_snip ?>
				</dl>
			</div> <!-- style-meta -->	
			<div class="style-example">
				<form class="form">
					<div class="form-row">
			            <label for="fileInput">File input</label>
			            <div class="input">
			              <input class="input-file" id="fileInput" name="fileInput" type="file">
						</div> <!-- /.input -->
					</div> <!-- /.form-row -->
				</form> <!-- /.form -->
			</div> <!-- style example --> 
		</li>

		<li class="style-node">
			<label class="style-node-h">Radio Buttons - List Format</label>
			<div class="style-meta-container">
				<dl class="style-meta">
					<?php echo $code_snip ?>
				</dl>
			</div> <!-- style-meta -->	
			<div class="style-example">
				<form class="form">
					<div class="form-row">
			            <label id="optionsRadio">List of options</label>
			            <div class="input">
			              <ul class="inputs-list">
			                <li>
			                  <label>
			                    <input type="radio" checked="" name="optionsRadios" value="option1">
			                    <span>Option one is this and that—be sure to include why it’s great</span>
			                  </label>
			                </li>
			                <li>
			                  <label>
			                    <input type="radio" name="optionsRadios" value="option2">
			                    <span>Option two can is something else and selecting it will deselect options 1</span>
			                  </label>
			                </li>
			              </ul> <!-- /.inputs-list -->
						</div> <!-- /.input -->
					</div> <!-- /.form-row -->
				</form> <!-- /.form -->
			</div> <!-- style example --> 
		</li>
	
		<li class="style-node">
			<label class="style-node-h">Checkboxes - List Format</label>
			<div class="style-meta-container">
				<dl class="style-meta">
					<?php echo $code_snip ?>
				</dl>
			</div> <!-- style-meta -->	
			<div class="style-example">
				<form class="form">
					<div class="form-row">
			            <label id="optionsCheckboxes">List of options</label>
			            <div class="input">
			              <ul class="inputs-list">
			                <li>
			                  <label>
			                    <input type="checkbox" name="optionsCheckboxes" value="option1">
			                    <span>Option one is this and that—be sure to include why it’s great</span>
			                  </label>
			                </li>
			                <li>
			                  <label>
			                    <input type="checkbox" name="optionsCheckboxes" value="option2">
			                    <span>Option two can also be checked and included in form results</span>
			                  </label>
			                </li>
			                <li>
			                  <label>
			                    <input type="checkbox" name="optionsCheckboxes" value="option2">
			                    <span>Option three can—yes, you guessed it—also be checked and included in form results. Let's make it super long so that everyone can see how it wraps, too.</span>
			                  </label>
			                </li>
			                <li>
			                  <label class="disabled">
			                    <input type="checkbox" name="optionsCheckboxes" value="option2" disabled="">
			                    <span>Option four cannot be checked as it is disabled.</span>
			                  </label>
			                </li>
			              </ul>
			              <span class="help-block">
			                <strong>Note:</strong> Labels surround all the options for much larger click areas and a more usable form.
			              </span>
              			</div> <!-- /.input -->
					</div> <!-- /.form-row -->
				</form> <!-- /.form -->
			</div> <!-- style example --> 
		</li>


		<li class="style-node">
			<label class="style-node-h">Inline Inputs</label>
			<div class="style-meta-container">
				<dl class="style-meta">
					<?php echo $code_snip ?>
				</dl>
			</div> <!-- style-meta -->	
			<div class="style-example">
				<form class="form">
					<div class="form-row">
			            <label>Date range</label>
			            <div class="input">
			              <div class="inline-inputs">
			                <input type="text" value="May 1, 2011">
			                <input type="text" value="12:00am">
			                to
			                <input type="text" value="May 8, 2011">
			                <input type="text" value="11:59pm">
			                <span class="help-block">All times are shown as Pacific Standard Time (GMT -08:00).</span>
			              </div> <!-- /.inline-inputs -->
              			</div> <!-- /.input -->
					</div> <!-- /.form-row -->
				</form> <!-- /.form -->
			</div> <!-- style example --> 
		</li>

		<li class="style-node">
			<label class="style-node-h">Disabled Input</label>
			<div class="style-meta-container">
				<dl class="style-meta">
					<?php echo $code_snip ?>
				</dl>
			</div> <!-- style-meta -->	
			<div class="style-example">
				<form class="form">
					<div class="form-row">
			            <label for="disabledInput">Disabled input</label>
			            <div class="input">
			              <input class="disabled" id="disabledInput" name="disabledInput" size="30" type="text" placeholder="Disabled input here… carry on." disabled="">
						</div> <!-- /.input -->
					</div> <!-- /.form-row -->
				</form> <!-- /.form -->
			</div> <!-- style example --> 
		</li>

		<li class="style-node">
			<label class="style-node-h">Disabled Textarea</label>
			<div class="style-meta-container">
				<dl class="style-meta">
					<?php echo $code_snip ?>
				</dl>
			</div> <!-- style-meta -->	
			<div class="style-example">
				<form class="form">
					<div class="form-row">
			            <label for="disabledInput">Disabled textarea</label>
			            <div class="input">
			              <textarea  name="textarea" id="textarea" rows="3" disabled=""></textarea>
						</div> <!-- /.input -->
					</div> <!-- /.form-row -->
				</form> <!-- /.form -->
			</div> <!-- style example --> 
		</li>
				
		<li class="style-node">
			<label class="style-node-h">Textarea with Block Help Text</label>
			<div class="style-meta-container">
				<dl class="style-meta">
					<dt>Description</dt>
					<dd>Help text provides the user with extra explanation where necessary</dd>
					<?php echo $code_snip ?>
				</dl>
			</div> <!-- style-meta -->	
			<div class="style-example">
				<form class="form">
					<div class="form-row">
			            <label for="textarea">Textarea with Block Help Text</label>
			            <div class="input">
			              <textarea  id="textarea2" name="textarea2" rows="3"></textarea>
			              <span class="help-block">
			                Block of help text to describe the field above if need be.
			              </span>
						</div> <!-- /.input -->
					</div> <!-- /.form-row -->
				</form> <!-- /.form -->
			</div> <!-- style example --> 
		</li>

		<li class="style-node">
			<label class="style-node-h">Text Input with Inline Help Text</label>
			<div class="style-meta-container">
				<dl class="style-meta">
					<dt>Description</dt>
					<dd>Help text provides the user with extra explanation where necessary</dd>
					<?php echo $code_snip ?>
				</dl>
			</div> <!-- style-meta -->	
			<div class="style-example">
				<form class="form">
					<div class="form-row">
			            <label for="help-input">Input with Inline Help</label>
			            <div class="input">
			              <input class="span-40" id="help-input" name="help-input" size="30" type="text">
			              <span class="help-inline">
			                Inline help text to describe input field.
			              </span>
						</div> <!-- /.input -->
					</div> <!-- /.form-row -->
				</form> <!-- /.form -->
			</div> <!-- style example --> 
		</li>

		<li class="style-node">
			<label class="style-node-h">Input with Error</label>
			<div class="style-meta-container">
				<dl class="style-meta">
					<dt>Note</dt>
					<dd>Add class of "error" to form-row</dd>
					<?php echo $code_snip ?>
				</dl>
			</div> <!-- style-meta -->	
			<div class="style-example">
				<form class="form">
					<div class="form-row error">
			            <label for="errorInput">Input with error</label>
			            <div class="input">
			              <input class="span-50" id="errorInput" name="errorInput" size="30" type="text">
			              <span class="help-inline">Small snippet of help text</span>
						</div> <!-- /.input -->
					</div> <!-- /.form-row -->
				</form> <!-- /.form -->
			</div> <!-- style example --> 
		</li>

		<li class="style-node">
			<label class="style-node-h">Input with Success</label>
			<div class="style-meta-container">
				<dl class="style-meta">
					<dt>Note</dt>
					<dd>Add class of "success" to form-row</dd>
					<?php echo $code_snip ?>
				</dl>
			</div> <!-- style-meta -->	
			<div class="style-example">
				<form class="form">
					<div class="form-row success">
			            <label for="successInput">Input with success</label>
			            <div class="input">
			              <input class="span-50" id="successInput" name="successInput" size="30" type="text">
			              <span class="help-inline">Success!</span>
						</div> <!-- /.input -->
					</div> <!-- /.form-row -->
				</form> <!-- /.form -->
			</div> <!-- style example --> 
		</li>

		<li class="style-node">
			<label class="style-node-h">Input with Warning</label>
			<div class="style-meta-container">
				<dl class="style-meta">
					<dt>Note</dt>
					<dd>Add class of "warning" to form-row</dd>
					<?php echo $code_snip ?>
				</dl>
			</div> <!-- style-meta -->	
			<div class="style-example">
				<form class="form">
					<div class="form-row warning">
			            <label for="warningInput">Input with warning</label>
			            <div class="input">
			              <input class="span-50" id="warningInput" name="warningInput" size="30" type="text">
			              <span class="help-inline">Ruh roh!</span>
						</div> <!-- /.input -->
					</div> <!-- /.form-row -->
				</form> <!-- /.form -->
			</div> <!-- style example --> 
		</li>

		<li class="style-node">
			<label class="style-node-h">Input with Prepended Text</label>
			<div class="style-meta-container">
				<dl class="style-meta">
					<dt>Note</dt>
					<dd>Useful when certain text will always be part of an input (i.e. - @ or %)</dd>
					<?php echo $code_snip ?>
				</dl>
			</div> <!-- style-meta -->	
			<div class="style-example">
				<form class="form">
					<div class="form-row">
			            <label for="prependedInput">Prepended text</label>
			            <div class="input">
			              <div class="input-prepend">
			                <span class="add-on">@</span>
			                <input id="prependedInput" name="prependedInput" size="16" type="text">
			              </div> <!-- /.input-prepend -->
			              <span class="help-block">Here's some help text</span>
			            </div> <!-- /.input -->
					</div> <!-- /.form-row -->
				</form> <!-- /.form -->
			</div> <!-- style example --> 
		</li>

		<li class="style-node">
			<label class="style-node-h">Input with Appended Text</label>
			<div class="style-meta-container">
				<dl class="style-meta">
					<dt>Note</dt>
					<dd>Useful when certain text will always be part of an input (i.e. - @ or %)</dd>
					<?php echo $code_snip ?>
				</dl>
			</div> <!-- style-meta -->	
			<div class="style-example">
				<form class="form">
					<div class="form-row">
			            <label for="appendedInput">Appended text</label>
			            <div class="input">
			              <div class="input-append">
			                <input id="appendedInput" name="appendedInput" size="16" type="text">
			                <span class="add-on">%</span>
			              </div> <!-- /.input-append -->
			              <span class="help-block">Here's some help text</span>
			            </div> <!-- /.input -->
					</div> <!-- /.form-row -->
				</form> <!-- /.form -->
			</div> <!-- style example --> 
		</li>

		<li class="style-node">
			<label class="style-node-h">Input with Prepended Checkbox</label>
			<div class="style-meta-container">
				<dl class="style-meta">
					<dt>Note</dt>
					<dd>Form elements can be appended, too</dd>
					<?php echo $code_snip ?>
				</dl>
			</div> <!-- style-meta -->	
			<div class="style-example">
				<form class="form">
					<div class="form-row">
			            <label for="prependedInput2">Prepended checkbox</label>
			            <div class="input">
			              <div class="input-prepend">
			                <label class="add-on"><input type="checkbox" name="" id="" value=""></label>
			                <input id="prependedInput2" name="prependedInput2" size="16" type="text">
			              </div> <!-- /.input-prepend -->
					</div> <!-- /.form-row -->
				</form> <!-- /.form -->
			</div> <!-- style example --> 
		</li>

		<li class="style-node">
			<label class="style-node-h">Form Actions</label>
			<div class="style-meta-container">
				<dl class="style-meta">
					<dt>Description</dt>
					<dd>Used at the bottom of form for submission, resetting, etc.</dd>
					<?php echo $code_snip ?>
				</dl>
			</div> <!-- style-meta -->	
			<div class="style-example">
				<form class="form">
		          <div class="form-actions">
		            <input type="submit" class="btn-dk" value="Save changes">&nbsp;<button type="reset" class="btn">Cancel</button>
		          </div>
				</form> <!-- /.form -->
			</div> <!-- style example --> 
		</li>

	</ul>
</div> <!-- style-container -->
