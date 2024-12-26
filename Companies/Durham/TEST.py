import re

# Sample HTML content
html_content = """

<div>
<div>
<div>
<div>
<div><strong>Interviews are expected to be held on Monday 25th November 2024</strong></div>

<div>&nbsp;</div>

<div><strong>The University &nbsp; &nbsp;</strong><br />
At Durham University, we are proud of our people, because they are at the heart of our globally outstanding institution, which is a key part of our local community. We inspire our people to do extraordinary things and we invite you to join our fantastic team. &nbsp; &nbsp;<br />
&nbsp; &nbsp;<br />
Across the University, we have a huge variety of roles and responsibilities, which together make us one large and successful community. Whether you are at the very start, middle or end of your career, there is a role for you. We believe everyone has their own unique skills to offer. &nbsp; &nbsp;<br />
&nbsp; &nbsp;<br />
At the University we promote and actively champion equality, diversity and inclusion. It is crucial that everyone can be themselves and can flourish in an environment where everyone respects each other and is treated fairly. We want our people and wider community to feel happy, secure and proud to be a part of Durham. We are looking for the same values in you. &nbsp; &nbsp;&nbsp;<br />
&nbsp; &nbsp;<br />
We welcome and encourage applications from members of groups who are under-represented in our work force including people with disabilities, women and black, Asian and minority ethnic communities. For more information on our EDI strategy and values,&nbsp;<a href="https://www.durham.ac.uk/about-us/professional-services/equality-diversity-inclusion/" rel="noopener" target="_blank">click here</a><br />
&nbsp; &nbsp;&nbsp;<br />
<strong>The Role and Department &nbsp;&nbsp;</strong><br />
The Computing and Information Services (CIS) has an annual operational budget in excess of &pound;12m, multi-million pound programmes of change within year, and approximately 185 staff. The Senior Leadership Team report directly to the Chief Information Officer (CIO) with the following portfolios: Strategy and Change; Technical Services; Information Services (IS), and Cyber Security. CIS work with departments across the university to provide academic, teaching and administrative services that underpin the day-to-day activities of the whole organisation. Details of the Digital Strategy and ongoing work can be found at&nbsp;<a href="https://www.durham.ac.uk/about-us/professional-services/computing-information-services/strategy/digital-strategy/" rel="noopener" target="_blank">Digital Strategy - Durham University</a>

<div>
<p>CIS is a friendly, but demanding department, where much is expected and can be achieved by competent, self-motivated individuals who are demonstrable in their team work ability. The department works in a hybrid capacity depending on the job role and individual personal requirements.</p>

<p>You will be sponsored to undertake a&nbsp;<strong>Level 3 &nbsp;Junior Developer</strong> apprenticeship. When undertaking your apprenticeship role, you will assist with activities to maintain the day to day operation and on-going development of Computing and Information Services (CIS). Assigned to one of the Information Systems (IS) teams, during the course of the apprenticeship you will maintain a high level of IT services throughout the University, assisting students, staff, visitors in their use of Durham University IT systems.</p>

<p>You will undertake and work with increasing independence in relation to:</p>

<p>&middot;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Software testing</p>

<p>&middot;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Software integration</p>

<p>&middot;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Software configuration</p>

<p>&middot;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Software support and troubleshooting</p>

<p>&middot;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Data and analytics</p>

<p>&middot;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;User experience analysis, design, and evaluation</p>

<p>&middot;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Content authoring and publishing</p>

<p>&middot;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Security operations</p>

<p>&middot;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Incident ownership and management&nbsp; &nbsp;</p>

<p>Further information about the role and the responsibilities is at the bottom of this job description. &nbsp;</p>

<p><strong>From early 2025 the base location for this role will change from our Durham City Centre site to our exciting new professional services hub based at Boldon House. Boldon House is situated on the outskirts of Durham near the Arnison Centre in Pity Me. Boldon House will bring a number of professional services teams together in a vibrant office environment which supports collaborative working and is designed to embrace hybrid working. To find out more about this project, please visit this webpage:&nbsp;</strong><a href="https://www.durham.ac.uk/about-us/estate-development/boldon-house/">Boldon House &ndash; Durham University</a><strong>.</strong></p>

<p>Further information about the role and the responsibilities is at the bottom of this job description. &nbsp;</p>

<p><strong>Working at Durham &nbsp; &nbsp;</strong><br />
A competitive salary is only one part of the many fantastic benefits you will receive if you join the University: you will also receive access to the following fantastic benefits: &nbsp; &nbsp;&nbsp;<br />
&bull;&nbsp;&nbsp; &nbsp;27 Days annual leave per year (in additional to 8 public holidays and 4 customary days per year), a total of 39 days. Including time off between Christmas and New Year &ndash; please include or delete if not applicable. &nbsp;&nbsp;<br />
&bull;&nbsp;&nbsp; &nbsp;No matter how you travel to work, we have you covered. &nbsp;We have parking across campus, a cycle to work scheme which helps you to buy a bike and discount with local bus and train companies. &nbsp;&nbsp;<br />
&bull;&nbsp;&nbsp; &nbsp;Discounts via our benefits portal including; money off at supermarkets, high street retailers, IT products such as Apple, the cinema and days out at various attractions. &nbsp; &nbsp;<br />
&bull;&nbsp; &nbsp;&nbsp;On site nursery is available plus access to holiday camps for children aged 5-16.<br />
&bull;&nbsp;&nbsp; &nbsp;Lots of support for health and wellbeing including discounted membership for our state of the art sport and gym facilities and access to a 24-7 Employee Assistance Programme. &nbsp; &nbsp;<br />
&bull;&nbsp;&nbsp; &nbsp;The opportunity to take part in staff volunteering activities. &nbsp;&nbsp;<br />
&bull;&nbsp;&nbsp; &nbsp;Family friendly policies, including maternity and adoption leave, which are among the most generous in the higher education sector (and likely above and beyond many employers) &nbsp; &nbsp;<br />
&bull;&nbsp;&nbsp; &nbsp;If you are keen on advancing in your role or career, we have a genuine passion for developing our colleagues &nbsp;from qualifications, to IT skills, courses and apprenticeships. &nbsp;&nbsp;<br />
&bull;&nbsp;&nbsp; &nbsp;Generous pension schemes.</p>

<p>Discover more about our total rewards and benefits package&nbsp;<a href="https://indd.adobe.com/view/898be764-ae6c-4c38-a3c9-ed120138f1b3">here</a></p>
</div>
</div>
</div>

<div>&nbsp;</div>
</div>
</div>
</div>

<div>
<div>
<div>
<div>
<div><strong>What you need to demonstrate when you apply</strong>

<div>
<p>To be considered for this role, here are the skills/experience we&rsquo;re looking for:</p>

<p><strong>ESSENTIAL CRITERIA:</strong></p>

<p><strong>Qualifications/Experience</strong></p>

<p>1.&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Five GCSE&rsquo;s at least Grade C or level four including English Language and Mathematics.&nbsp;</p>

<p>2.&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Experience of working in a team in a services or IT provision area or having relevant qualifications for the role.</p>

<p>3.&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Experience of managing time to meet deadlines.</p>

<p><strong>Skills/Abilities/Knowledge</strong></p>

<p>4.&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Good spoken and written communication skills.</p>

<p>5.&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Good digital skills including experience in using digital devices and apps including the internet, email, digital communication tools, Microsoft 365 applications, digital booking systems</p>

<p>6.&nbsp; &nbsp; Committed to ongoing training/continuing professional development</p>

<p>7.&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Ability to solve problems as part of a team and resolve straightforward issues.</p>

<p>8.&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Ability to provide advice and guidance to a range of colleagues and customers.</p>

<p>9.&nbsp; &nbsp;&nbsp;Basic level of software coding gained either within an educational setting, or from a previous employment, or through a&nbsp; &nbsp;hobby related interest</p>

<p><strong>DESIRABLE CRITERIA:</strong></p>

<p>&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;10.&nbsp; &nbsp; Knowledge of health and safety issues such as risk assessments.</p>

<p>&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;11.&nbsp; &nbsp; Ability to provide support for projects</p>

<p><strong>How to Apply &nbsp; &nbsp;&nbsp;</strong><br />
&nbsp; &nbsp;&nbsp;<br />
<u>Submitting your application</u><br />
&nbsp;&nbsp;<br />
We prefer to receive applications online. We will update you about your application at various points throughout the selection process, via automated emails from our e-recruitment system. Please check your spam/junk folder periodically to make sure you have not missed any of our updates. &nbsp;<br />
&nbsp; &nbsp;&nbsp;<br />
<strong>What you must submit:</strong></p>

<p>An up-to-date CV</p>

<p><strong>AND</strong></p>

<p>A cover letter explaining what interests you about the role</p>

<p><strong>AND</strong></p>

<p>A supporting statement which clearly&nbsp;outlines how you meet <strong>each individual</strong>&nbsp;Essential&nbsp;criteria within the Person Specification (above); when submitting evidence of each essential criteria, please ensure you use the essential criteria wording as the section heading.</p>

<p><strong>Who to contact for more information &nbsp;&nbsp;</strong><br />
If you would like to have a chat or ask any questions about the role or if you are struggling to complete the application process,&nbsp;Catherine Wilson (<a href="mailto:rashad.mahmood@durham.ac.uk">Catherine.Wilson@durham.ac.uk</a>)&nbsp;would be happy to speak to you.<br />
&nbsp;&nbsp;<br />
<strong>Specific role requirements</strong></p>

<p>1.&nbsp;&nbsp;&nbsp;To be eligible to apply for an apprenticeship position,&nbsp;<em>there are specific requirements in order to receive the funding&nbsp;and,&nbsp;</em>you must not have obtained a higher education qualification at Level 4 or above as defined on the NQF or QCF, including being awarded a first degree by a recognised university or other recognised higher education institution, with the exception of anyone who has participated in New Deal. In order to fulfil the terms and conditions of the apprenticeship, the post-holder will be required to complete training on a weekly basis towards a Level 3.</p>

<p>2.&nbsp;&nbsp;&nbsp;Whilst working within IS the hours of service are currently 8.00 am to 6.00 pm Monday to Friday but a flexible approach to work will be required to ensure that all duties are covered, especially at times of a major incident or software upgrade. Occasional evening and weekend work may be required.</p>

<p>3.&nbsp;&nbsp;&nbsp;Whilst working within IS there is a four-week annual leave ban in place at the start of the academic year Sept/Oct to support staff and students over that known busy period.</p>

<p><strong>Typical Role Requirements &nbsp;&nbsp;</strong></p>

<p>Here are the kind of activities that you&rsquo;ll be asked to undertake and ways in which you&rsquo;ll be expected to operate.</p>

<p><strong>Service Delivery</strong><br />
&bull; &nbsp; &nbsp;Provide an excellent service to our students, your colleagues and anyone else you come across as part of your role by carrying out your tasks using the relevant procedures (which we will provide training for).<br />
&bull; &nbsp; &nbsp;Look after yourself and others by following health and safety regulations including correctly wearing any protective clothing or equipment provided e.g. safety shoes, being aware of any hazards and risks and reporting any incidents.<br />
&bull; &nbsp; &nbsp;Carry out some tasks that may require specialist skills and may be physically demanding &ndash; please remove if not applicable.<br />
&bull; &nbsp; &nbsp;Clean and look after specialist equipment and tools&nbsp;when necessary.</p>

<p><!-- [if !supportLists]-->&middot;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <!--[endif]-->Follow established procedures when carrying out your role and vary or refer to more senior colleagues when necessary.</p>

<p><!-- [if !supportLists]-->&middot;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <!--[endif]-->Collect, organise and record data accurately for use by others and provide reports where required.</p>

<p><strong>Teamwork</strong><br />
&bull; &nbsp; &nbsp;Help and cooperate with the rest of your team&nbsp;<!--[endif]-->on operational matters to help achieve shared objectives.<em><strong>&nbsp;</strong></em></p>

<p>&bull; &nbsp; &nbsp;Help your colleagues when required with other key activities undertaken within your service.<br />
&bull; &nbsp; &nbsp;Help to move, set-up and dismantle any equipment or tools.<br />
&bull; &nbsp; &nbsp;Learn new skills and practices from more experienced colleagues.<br />
&bull; &nbsp; &nbsp;Bring any problems to the attention of more senior colleagues.</p>

<p><!-- [if !supportLists]-->&middot;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <!--[endif]-->Liaise with staff in other areas to ensure that services are being delivered in an efficient and collaborative way.</p>

<p><br />
&nbsp;<strong>Communication/Personal&nbsp;</strong><br />
&bull; &nbsp; &nbsp;Show a commitment to equality, diversity and inclusion and the University&rsquo;s values.<br />
&bull; &nbsp; &nbsp;Respond to routine requests for information.<br />
&bull; &nbsp; &nbsp;Use digital devices and apps (such as email) to communicate with students, your colleagues and anyone else you come across as part of your role.</p>

<p>&bull; &nbsp; &nbsp;Any other reasonable duties.</p>

<p>Please note that in submitting your application Durham University will be processing your data. We would ask you to consider the relevant University Privacy Statement&nbsp;<a href="https://www.durham.ac.uk/about-us/governance/information-governance/privacy-notices/job-applicants/">Privacy Notices - Durham University</a>&nbsp;which provides information on the collation, storing and use of data. &nbsp; &nbsp;&nbsp;</p>
</div>
</div>
</div>
</div>
</div>
</div>


"""

# # Define the pattern for splitting based on closing tags and <br> tags
# pattern = r'(<\/\w+>|<br\s*\/?>)'
# split_content = re.split(pattern, html_content)
# for part in split_content:
#     print(part)



# Define the pattern for identifying the bullet points and sub points
bullet_pattern = r'(&bull;|&middot;)\s*&nbsp;\s*&nbsp;'

# Function to convert matched lines to list elements
def convert_to_list_elements(content):
    # Find lines containing the bullet points or sub-points
    content = re.sub(bullet_pattern, '', content)  # Remove the bullet pattern
    content = f'<ul><li>{content.strip()}</li></ul>'  # Wrap content in <ul><li></li></ul>
    return content

# Split content based on lines and process each one
split_content = re.split(r'(<\/\w+>|<br\s*\/?>)', html_content)

# Process the split content
processed_content = []

for part in split_content:
    if re.search(bullet_pattern, part):
        # If the part matches the bullet pattern, convert it to a list element
        processed_content.append(convert_to_list_elements(part))
    else:
        # Otherwise, just add the original part (it could be a paragraph, text, etc.)
        processed_content.append(part)

# Join the processed content into a single string
final_content = ''.join(processed_content)

# Output the final HTML content
# print(final_content)

print("result =\n\n\n\n\n\n",final_content)