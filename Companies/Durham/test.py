import re

class HTMLProcessor:
    def remove_inline_styles(self, html_content):
        # Remove inline styles
        html_content = re.sub(r'style="[^"]*"', '', html_content)
        
        # Remove empty tags (with or without inner content)
        empty_tag_pattern = r'<(\w+)(\s+[^>]*)?>\s*(<\w+>\s*</\w+>\s*)*\s*</\1>'
        html_content = re.sub(empty_tag_pattern, '', html_content)
        
        # Convert the content with <!-- [if !supportLists]--> into <li> items
        regex = r'<!-- \[if !supportLists\]-->&middot;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;([^<]+?)<!--\[endif\]-->'
        converted_html = re.sub(regex, r'<li>\1</li>', html_content)
        
        # Remove any <p> tags that do not contain valid content (empty or whitespace-only)
        converted_html = re.sub(r'<p>\s*</p>', '', converted_html)

        # Wrap the converted <li> items in a <ul> tag
        final_html = f'<ul>{converted_html}</ul>'
        
        return final_html

# Sample usage
html_content = '''
<p><strong>Job Title</strong>:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Maintenance Electrician</p>

<p><strong>Department</strong>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Estates and Facilities</p>

<p><strong>Grade:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; </strong>Grade 5</p>

<p><strong>Salary range:</strong> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Up to &pound;29,659</p>

<p><strong>Working arrangements:</strong>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Permanent</p>

<p><strong>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; </strong>Full time (35 hours)</p>

<p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Onsite working only</p>

<p><strong>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; </strong>Participation in an on-call rota for out of hours cover</p>

<p><strong>Closing date:</strong>&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;Saturday 30th November 2024</p>

<p><strong>Shortlisting and interviews will take place throughout the advertising period and if it is possible to fill the vacancies before the closing date, the advert will close immediately</strong></p>

<p>&nbsp;</p>

<p><strong>The University</strong></p>

<p>At Durham University we are proud of our people.&nbsp; A globally outstanding centre of educational excellence, a collegiate community of extraordinary people, a unique and historic setting &ndash; Durham is a university like no other.&nbsp; Across the University we have a huge variety of roles and career opportunities, which together make us a large and successful community, which is a key hub of activity within our region and nationally.&nbsp; Whether you are at the very start, middle or end of your career, there is a role for you.&nbsp; We believe everyone has their own unique skills to offer.&nbsp; We would be thrilled if you would consider joining our thriving University.</p>

<p>&nbsp;</p>

<p>Further information about the University can be found <a href="https://www.durham.ac.uk/homepage/">here</a>.</p>

<p>&nbsp;</p>

<p><strong>The Role and Department</strong></p>

<p>It is an exciting time to join the Estates and Facilities Directorate, as we are currently delivering an ambitious programme of works, to deliver a new estate; supporting the University&rsquo;s overarching strategy, with the design and construction of new teaching, leisure and accommodation facilities, alongside the repair and refurbishments to the existing infrastructure and buildings</p>

<p>As a member of the Estates and Facilities Directorate directly employed labour team, you will undertake electrical repairs and maintenance work, to an agreed level, in compliance with industry standards, statutory requirements, relevant codes of practice in a professional and customer-focused manner.</p>

<p>The Estates and Facilities Directorate provides essential services to Durham University and is responsible for managing, maintaining and developing the infrastructure and building fabric of the various campuses.</p>

<p>Further information about the role and the responsibilities is at the bottom of this job description.</p>

<p>&nbsp;</p>

<p><strong>Working at Durham</strong></p>

<p>&nbsp;</p>

<p>A competitive salary is only one part of the many fantastic benefits you will receive if you join the University, you will also receive access to the following fantastic benefits:</p>

<p>&nbsp;</p>

<p><!-- [if !supportLists]-->&middot;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <!--[endif]-->27 days annual leave per year in addition to 8 public holidays and 4 customary days per year (39 days per year).&nbsp; The University closes between Christmas and New Year.</p>

<p><!-- [if !supportLists]-->&middot;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <!--[endif]-->No matter how you travel to work, we have you covered.&nbsp; We have parking across campus, a cycle to work scheme which helps you to buy a bike and discount with local bus and train companies.</p>

<p><!-- [if !supportLists]-->&middot;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <!--[endif]-->Lots of support for health and wellbeing including discounted membership for our state-of-the-art sport and gym facilities and access to a 24-7 Employee Assistance Programme.</p>

<p><!-- [if !supportLists]-->&middot;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <!--[endif]-->On site nursery is available and children&rsquo;s clubs in the summer holidays.</p>

<p><!-- [if !supportLists]-->&middot;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <!--[endif]-->Family friendly policies, including maternity and adoption leave, which are among the most generous in the higher education sector (and likely above and beyond many employers).</p>

<p><!-- [if !supportLists]-->&middot;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <!--[endif]-->There is a genuine commitment to developing our colleagues professionally and personally.&nbsp; There is a comprehensive range of development courses, apprenticeships and access to qualifications and routes to develop your career in the University.&nbsp; All staff have dedicated annual time to concentrate on their personal development opportunities.</p>

<p><!-- [if !supportLists]-->&middot;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <!--[endif]-->The opportunity to take part in staff volunteering activities to make a difference in the local community.</p>

<p><!-- [if !supportLists]-->&middot;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <!--[endif]-->Discounts are available via our benefits portal including money off at supermarkets, high street retailers, IT products such as Apple, the cinema and days out at various attractions.</p>

<p><!-- [if !supportLists]-->&middot;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <!--[endif]-->We offer generous pension schemes.</p>

<p>&nbsp;</p>

<p><strong>Durham University is committed to equality diversity, inclusion and values</strong></p>

<p>&nbsp;</p>

<p>Our collective aim is to create an open and inclusive environment where everyone can reach their full potential and we believe our staff should reflect the diversity of the global community in which we work.</p>

<p>&nbsp;</p>

<p>As a University, equality, diversity, and inclusion (EDI) are a key part of the University&rsquo;s Strategy and a central part of everything we do. &nbsp;We also live by our <a href="https://www.dur.ac.uk/about/values/">values</a> and our <a href="https://www.durham.ac.uk/media/durham-university/professional-services/job-vacancies/job-descriptions/STAFF-CODE-OF-CONDUCT.pdf">Staff Code of Conduct.</a>&nbsp; At Durham we actively work towards providing an environment where our staff and students can study, work and live in a community which is supportive and inclusive. &nbsp;It&rsquo;s important to us that all of our colleagues are aligned to both our values and commitment to EDI.</p>

<p> </p>

<p>We welcome and encourage applications from members of groups who are under-represented in our work force including people with disabilities, women and black, Asian and minority ethnic communities.&nbsp; If you have taken time out of your career, and you feel it relevant, let us know about it in your application.&nbsp; If you are a candidate with a disability, we are committed to ensuring fair treatment throughout the recruitment process. &nbsp;We will make adjustments to support the interview process wherever it is reasonable to do so and, where successful, reasonable adjustments will be made to support people within their role.</p>

<p><strong>What you need to demonstrate when you apply/Person Specification</strong></p>

<p>&nbsp;</p>

<p>When you apply it is important that you let us know what skills/experience you have from a similar role and/or what skills/experience you have which would make you right for this role.  Further information about the role and responsibilities is at the end of this job description.</p>

<p>&nbsp;</p>

<p>Your application should cover the followingcriteria:</p>

<p>&nbsp;</p>

<p><strong>Essential Criteria</strong></p>

<p>&nbsp;</p>

<p><strong>Qualifications/Experience</strong></p>

<p><!-- [if !supportLists]-->1.&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <!--[endif]-->Five GCSEs at least Grade C or level four (or equivalent) including English Language and Mathematics or a Post-16 qualification or equivalent experience.</p>

<p><!-- [if !supportLists]-->2.&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <!--[endif]-->CITB apprenticeship or other relevant approved training.</p>

<p><!-- [if !supportLists]-->3.&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <!--[endif]-->Professional craftsperson/practitioner with knowledge and expertise in one or more areas of buildings or estates services.</p>

<p><!-- [if !supportLists]-->4.&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <!--[endif]-->Experience of working within a team to ensure the delivery of high-quality services.</p>

<p><!-- [if !supportLists]-->5.&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <!--[endif]-->Experience of contributing to the delivery of electrical services in residential and educational buildings. &nbsp;</p>

<p><!-- [if !supportLists]-->6.&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <!--[endif]-->Experience of providing advice and guidance to a range of customers and colleagues</p>

<p><!-- [if !supportLists]-->7.&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <!--[endif]-->Experience of managing time to meet deadlines.</p>

<p><!-- [if !supportLists]-->8.&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <!--[endif]-->Interpretation of work to be undertaken as outlined in routine instruction, drawings and specifications.</p>

<p><!-- [if !supportLists]-->9.&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <!--[endif]-->Experience of diagnosing and repairing faults in electrical services installations and estimating material requirements.</p>

<p><!-- [if !supportLists]-->10.&nbsp;&nbsp; <!--[endif]-->Completion of maintenance documentation and related records.</p>

<p><strong>&nbsp;</strong></p>

<p><strong>Skills/Abilities/Knowledge</strong></p>

<p><!-- [if !supportLists]-->11.&nbsp;&nbsp; <!--[endif]-->Excellent spoken and written communication skills and the ability to develop effective working relationships, both internally and externally.</p>

<p><!-- [if !supportLists]-->12.&nbsp;&nbsp; <!--[endif]-->Strong digital competence across a range of digital devices and apps including digital communication tools, Microsoft 365 applications, digital booking system, project planning tools.</p>

<p><!-- [if !supportLists]-->13.&nbsp;&nbsp; <!--[endif]-->Industry or professional knowledge and recognition relevant to the role supported by relevant courses or certification, such as 18th edition of the IEE Regulations and advanced certificate in electrical installations, Construction Skills Certificate Scheme or equivalent.</p>

<p><!-- [if !supportLists]-->14.&nbsp;&nbsp; <!--[endif]-->Ability to solve problems and resolve issues using own initiative, plan solutions and make pragmatic decisions with minimal supervision.</p>

<p><!-- [if !supportLists]-->15.&nbsp;&nbsp; <!--[endif]-->Ability to provide support for infrastructure projects.</p>

<p><!-- [if !supportLists]-->16.&nbsp;&nbsp; <!--[endif]-->Health and safety compliance knowledge, including risk assessments and method statements.</p>

<p><!-- [if !supportLists]-->17.&nbsp;&nbsp; <!--[endif]-->Ability to use and operate the usual range of tools and equipment associated with the trade.</p>

<p><!-- [if !supportLists]-->18.&nbsp;&nbsp; <!--[endif]-->Achieving service delivery and performance goals.</p>

<p><!-- [if !supportLists]-->19.&nbsp;&nbsp; <!--[endif]-->Flexible attitude to multi-skilled maintenance tasks, designed to maximise operational effectiveness.</p>

<p><strong>&nbsp;</strong></p>

<p><strong>&nbsp;</strong></p>

<p><strong>Desirable Criteria</strong></p>

<p><strong>&nbsp;</strong></p>

<p><!-- [if !supportLists]-->1.&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <!--[endif]-->Evidence of continuing professional development.</p>

<p><!-- [if !supportLists]-->2.&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <!--[endif]-->Evidence of working in occupied properties, historic and listed buildings.</p>

<p><!-- [if !supportLists]-->3.&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <!--[endif]-->Ability to provide support for infrastructure projects.</p>

<p><!-- [if !supportLists]-->4.&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <!--[endif]-->Ability to effectively network and exchange advice and information for development purposes.</p>

<p>&nbsp;</p>

<p><strong>How to apply</strong></p>

<p>&nbsp;</p>

<p>To progress to the assessment stage, candidates must evidence each of the essential criteria required for the role in the person specification above.&nbsp; Where there are desirable criteria, we would also urge you to provide any relevant evidence.</p>

<p>&nbsp;</p>

<p>While some criteria will be considered at the shortlisting stage, other criteria may be considered later in the assessment process, such as questions at interview.</p>

<p>&nbsp;</p>

<p><strong>Submitting your application</strong></p>

<p>&nbsp;</p>

<p>We prefer to receive applications online.&nbsp; We will update you about your application at various points throughout the selection process, via automated emails from our e-recruitment system. Please check your spam/junk folder periodically to ensure you receive all emails.</p>

<p>&nbsp;</p>

<p><strong>&nbsp;</strong></p>

<p><strong>What you are required to submit</strong></p>

<p>&nbsp;</p>

<p><!-- [if !supportLists]-->&middot;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <!--[endif]-->A CV</p>

<p><!-- [if !supportLists]-->&middot;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <!--[endif]-->A supporting statement/covering letter, which shows examples of how you meet all of the criteria within the Person Specification.</p>

<p><strong>&nbsp;</strong></p>

<p><strong>Contact details</strong></p>

<p>&nbsp;</p>

<p>If you would like to have a chat or ask any questions about the role, David Profit, Senior Maintenance Services Manager, <a href="mailto:david.profit@durham.ac.uk">david.profit@durham.ac.uk</a>, would be happy to speak to you.</p>

<p>&nbsp;</p>

<p><strong>Typical Role Requirements</strong></p>

<p>&nbsp;</p>

<p><strong>Service Delivery</strong></p>

<p><!-- [if !supportLists]-->&middot;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <!--[endif]-->Resolve queries and requests for information and advice and escalate more specialist and complex queries or issues to more experienced team members, completing the appropriate electronic and/or hardcopy work orders.</p>

<p><!-- [if !supportLists]-->&middot;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <!--[endif]-->Identify priorities and monitor processes and activities to ensure success.</p>

<p><!-- [if !supportLists]-->&middot;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <!--[endif]-->Show a commitment to equality, diversity and inclusion and the University&rsquo;s values.</p>

<p><!-- [if !supportLists]-->&middot;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <!--[endif]-->When carrying out your role, apply recognised industry professional procedures and techniques, to ensure that our facilities are safe, secure and appropriate for public access and use.</p>

<p><!-- [if !supportLists]-->&middot;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <!--[endif]-->Respond to queries and provide information/advice, while raising more specialist or complex queries with more experienced team members.</p>

<p><!-- [if !supportLists]-->&middot;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <!--[endif]-->Use your experience and problem-solving skills to investigate and resolve issues relevant to your role.</p>

<p><!-- [if !supportLists]-->&middot;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <!--[endif]-->Analyse work activities to ensure the effective and efficient use of capital and consumable equipment and resources. Provide more in-depth independent research and analysis activities within the role.</p>

<p><!-- [if !supportLists]-->&middot;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <!--[endif]-->Make recommendations into work processes and report analysis of patterns and trends in work activities for consideration to senior colleagues.</p>

<p><!-- [if !supportLists]-->&middot;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <!--[endif]-->Manage and monitor the use of components, resources and equipment.</p>

<p><!-- [if !supportLists]-->&middot;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <!--[endif]-->Deliver infrastructure support services relating to administrative, business, teaching, research and learning to support the University&rsquo;s activities.</p>

<p><!-- [if !supportLists]-->&middot;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <!--[endif]-->Prepare safety documents, to meet security and safety requirements.</p>

<p><!-- [if !supportLists]-->&middot;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <!--[endif]-->Continually review what is required from staff, students and others who you work with to make sure the best possible service is provided.</p>

<p><!-- [if !supportLists]-->&middot;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <!--[endif]-->Prepare safety documents and risk assessments relating to activities across theestate.</p>

<p><!-- [if !supportLists]-->&middot;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <!--[endif]-->Undertake all electrical work across the estate, appropriate to the grade, including day-to-day repairs and planned maintenance, and installation and testing of statutory equipment.</p>

<p>&nbsp;</p>

<p><strong>Planning and Organising</strong></p>

<p><!-- [if !supportLists]-->&middot;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <!--[endif]-->Plan and organise own workload with or without involvement with project work streams to deliver the role.</p>

<p><!-- [if !supportLists]-->&middot;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <!--[endif]-->Organise and schedule assigned resources, including stock control.</p>

<p><!-- [if !supportLists]-->&middot;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <!--[endif]-->Monitor processes and activities to ensure team priorities are met.</p>

<p><!-- [if !supportLists]-->&middot;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <!--[endif]-->Help to plan and evaluate the services provided by your area to ensure that requirements from your service are being met. Assist colleagues to achieve operational requirements.</p>

<p><strong>&nbsp;</strong></p>

<p><strong>&nbsp;</strong></p>

<p><strong>Teamwork</strong></p>

<p><!-- [if !supportLists]-->&middot;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <!--[endif]-->Provide specialist support and advice to team members on areas of expertise.</p>

<p><!-- [if !supportLists]-->&middot;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <!--[endif]-->Make changes to the services provided by your team in discussion with other team members.</p>

<p><!-- [if !supportLists]-->&middot;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <!--[endif]-->Identify opportunities and contribute to decisions on how to improve services being delivered by the team.</p>

<p><!-- [if !supportLists]-->&middot;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <!--[endif]-->Seek feedback from students, staff and anyone else that you come across as part of your role on their requirements from your service and recommend improvements to senior colleagues.</p>

<p><strong>&nbsp;</strong></p>

<p><strong>Communication/Liaison</strong></p>

<p><!-- [if !supportLists]-->&middot;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <!--[endif]-->Use your knowledge and expertise to provide advice and guidance to resolve problems and respond to a wide range of queries.</p>

<p><!-- [if !supportLists]-->&middot;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <!--[endif]-->Provide instruction and demonstration to others within an area of working beyond immediate team.</p>

<p><!-- [if !supportLists]-->&middot;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <!--[endif]-->Explain and demonstrate tasks to others to ensure that components, equipment and processes are used correctly.</p>

<p><!-- [if !supportLists]-->&middot;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <!--[endif]-->Create good working relationships with other team members and anyone else that you come across as part of your role to work together on joint activities.</p>

<p><!-- [if !supportLists]-->&middot;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <!--[endif]-->Create good working relationships with internal and external partners and suppliers to work together on joint activities.</p>

<p><!-- [if !supportLists]-->&middot;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <!--[endif]-->Build relationships with contacts and contribute to internal and external networks to share good practice and exchange information.</p>

<p><!-- [if !supportLists]-->&middot;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <!--[endif]-->Liaise with outside agencies, local authorities, suppliers and visitors to ensure that services are safe and secure.&nbsp;</p>

<p><!-- [if !supportLists]-->&middot;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <!--[endif]-->Any other reasonable duties.</p>

<p>&nbsp;</p>

<p>Please note that in submitting your application Durham University will be processing your data. We would ask you to consider the relevant <a href="https://www.dur.ac.uk/ig/dp/privacy/pnjobapplicants/">University Privacy Statement</a>, which provides information on the collation, storing and use of data.</p>

<p>&nbsp;</p>

<p>When appointing to this role the University must ensure that it meets any applicable immigration requirements, including salary thresholds which are applicable to some visas.</p>

<ul>
</ul>
'''

processor = HTMLProcessor()
result = processor.remove_inline_styles(html_content)
print(result)
