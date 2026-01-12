"""
Management command to populate the database with sample content
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from core.models import SliderItem, AboutSection, TeamMember, ContactInfo
from education.models import EducationCategory, Article, ExamMaterial
from games.models import GameType, Game, GameQuestion, GameAnswer
from cases.models import LegalCase
from news.models import NewsCategory, NewsArticle

User = get_user_model()


class Command(BaseCommand):
    help = 'Populates the database with sample content'

    def handle(self, *args, **options):
        self.stdout.write('Starting to populate content...')
        
        # Create Contact Info
        contact_info, created = ContactInfo.objects.get_or_create(
            defaults={
                'address': '123 Legal Street, Law District\nCity, Country 12345',
                'phone': '+1 (555) 123-4567',
                'email': 'info@legallaboratory.com',
                'facebook': 'https://facebook.com/legallab',
                'linkedin': 'https://linkedin.com/company/legallab',
                'twitter': 'https://twitter.com/legallab',
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS('[OK] Contact info created'))
        
        # Create Slider Items
        slider_items = [
            {
                'title': 'Welcome to Legal Laboratory',
                'description': 'Your comprehensive platform for legal education and professional development',
                'button_text': 'Start Learning',
                'button_link': '/education/',
                'order': 1,
            },
            {
                'title': 'Interactive Legal Games',
                'description': 'Learn through gamified experiences and test your legal knowledge',
                'button_text': 'Play Games',
                'button_link': '/games/',
                'order': 2,
            },
            {
                'title': 'Case Analysis Laboratory',
                'description': 'Practice with real and simulated legal cases to enhance your skills',
                'button_text': 'Explore Cases',
                'button_link': '/cases/',
                'order': 3,
            },
        ]
        
        for item_data in slider_items:
            item, created = SliderItem.objects.get_or_create(
                title=item_data['title'],
                defaults=item_data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'[OK] Slider item created: {item_data["title"]}'))
        
        # Create About Sections
        about_sections = [
            {
                'title': 'Our Mission',
                'content': 'Legal Laboratory is dedicated to providing comprehensive legal education through innovative platforms that combine theoretical knowledge with practical application. We aim to bridge the gap between academic learning and real-world legal practice, empowering students and professionals to excel in their legal careers.',
                'order': 1,
            },
            {
                'title': 'Our Vision',
                'content': 'To become the leading platform for legal education and professional development, recognized for excellence in gamified learning, practical case analysis, and professional networking. We envision a future where legal education is accessible, engaging, and directly applicable to real-world scenarios.',
                'order': 2,
            },
            {
                'title': 'Core Values',
                'content': 'Excellence: We maintain the highest standards in all our educational content and services.\n\nInnovation: We continuously explore new methods and technologies to enhance learning experiences.\n\nAccessibility: We believe legal education should be available to all who seek it.\n\nPracticality: We focus on real-world applications and practical skills development.',
                'order': 3,
            },
        ]
        
        for section_data in about_sections:
            section, created = AboutSection.objects.get_or_create(
                title=section_data['title'],
                defaults=section_data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'[OK] About section created: {section_data["title"]}'))
        
        # Create Team Members
        team_members = [
            {
                'name': 'Dr. Sarah Johnson',
                'position': 'Chief Legal Educator',
                'bio': 'With over 20 years of experience in legal education, Dr. Johnson specializes in criminal law and procedure. She has authored numerous legal textbooks and is a recognized expert in legal pedagogy.',
                'email': 'sarah.johnson@legallab.com',
                'order': 1,
            },
            {
                'name': 'Prof. Michael Chen',
                'position': 'Senior Legal Analyst',
                'bio': 'Professor Chen is an expert in civil law and judicial practice. He has served as a consultant for various legal institutions and has extensive experience in case analysis and legal research.',
                'email': 'michael.chen@legallab.com',
                'order': 2,
            },
            {
                'name': 'Attorney Lisa Martinez',
                'position': 'Legal Practice Director',
                'bio': 'Attorney Martinez brings practical courtroom experience to our platform. With 15 years as a practicing lawyer, she provides real-world insights and practical guidance to our students.',
                'email': 'lisa.martinez@legallab.com',
                'order': 3,
            },
        ]
        
        for member_data in team_members:
            member, created = TeamMember.objects.get_or_create(
                name=member_data['name'],
                defaults=member_data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'[OK] Team member created: {member_data["name"]}'))
        
        # Create Education Categories
        education_categories = [
            {
                'name': 'Criminal Law',
                'icon': '⚖️',
                'description': 'Comprehensive study of criminal law, offenses, and penalties',
                'order': 1,
            },
            {
                'name': 'Criminal Procedure',
                'icon': '📋',
                'description': 'Legal procedures in criminal cases from investigation to trial',
                'order': 2,
            },
            {
                'name': 'Civil Law',
                'icon': '📜',
                'description': 'Civil rights, contracts, torts, and property law',
                'order': 3,
            },
            {
                'name': 'Judicial Practice',
                'icon': '🏛️',
                'description': 'Court procedures, evidence, and judicial decision-making',
                'order': 4,
            },
        ]
        
        categories_dict = {}
        for cat_data in education_categories:
            category, created = EducationCategory.objects.get_or_create(
                name=cat_data['name'],
                defaults=cat_data
            )
            categories_dict[cat_data['name']] = category
            if created:
                self.stdout.write(self.style.SUCCESS(f'[OK] Education category created: {cat_data["name"]}'))
        
        # Create Articles
        articles = [
            {
                'category': categories_dict['Criminal Law'],
                'title': 'Understanding Criminal Intent: Mens Rea Explained',
                'slug': 'understanding-criminal-intent-mens-rea',
                'content': '''Criminal intent, or mens rea, is a fundamental concept in criminal law that refers to the mental state of a person when committing a crime. This article explores the different levels of mens rea and their implications in criminal proceedings.

## Levels of Mens Rea

### 1. Purposefully (Intentional)
When a person acts purposefully, they have a conscious objective to engage in conduct or cause a result. This is the highest level of criminal intent.

### 2. Knowingly
A person acts knowingly when they are aware that their conduct is of a certain nature or that certain circumstances exist.

### 3. Recklessly
Reckless conduct involves a conscious disregard of a substantial and unjustifiable risk.

### 4. Negligently
Negligent conduct involves a failure to be aware of a substantial and unjustifiable risk.

## Practical Applications

Understanding mens rea is crucial for:
- Proper case analysis
- Defense strategies
- Prosecution arguments
- Jury instructions

This knowledge is essential for anyone working in the criminal justice system.''',
                'excerpt': 'Explore the fundamental concept of criminal intent and its various levels in criminal law proceedings.',
                'author': 'Dr. Sarah Johnson',
            },
            {
                'category': categories_dict['Criminal Procedure'],
                'title': 'The Right to Counsel: A Comprehensive Guide',
                'slug': 'right-to-counsel-comprehensive-guide',
                'content': '''The right to counsel is one of the most important constitutional rights in criminal procedure. This article examines when this right attaches and how it applies in various stages of criminal proceedings.

## When the Right Attaches

The Sixth Amendment guarantees the right to counsel in all criminal prosecutions. This right attaches at critical stages, including:
- Initial appearance
- Preliminary hearings
- Arraignment
- Trial
- Sentencing

## Miranda Rights

The famous Miranda warning stems from the right to counsel and the right against self-incrimination. Understanding when Miranda applies is crucial for law enforcement and defense attorneys.

## Effective Assistance of Counsel

The right to counsel includes the right to effective assistance. This means counsel must provide competent representation, and failure to do so can result in reversal of convictions.

## Practical Implications

This right affects:
- Police interrogations
- Court proceedings
- Appeal strategies
- Defendant rights''',
                'excerpt': 'A detailed examination of the constitutional right to counsel and its application in criminal cases.',
                'author': 'Prof. Michael Chen',
            },
            {
                'category': categories_dict['Civil Law'],
                'title': 'Contract Law Fundamentals: Offer and Acceptance',
                'slug': 'contract-law-fundamentals-offer-acceptance',
                'content': '''Contract law forms the foundation of commercial transactions. This article covers the essential elements of contract formation, focusing on offer and acceptance.

## Elements of a Contract

A valid contract requires:
1. Offer
2. Acceptance
3. Consideration
4. Legal capacity
5. Legal purpose

## The Offer

An offer is a proposal to enter into a contract. It must be:
- Definite and certain
- Communicated to the offeree
- Made with intent to be bound

## Acceptance

Acceptance must be:
- Unconditional
- Communicated to the offeror
- Made before the offer expires

## Common Issues

Understanding these concepts helps in:
- Drafting contracts
- Dispute resolution
- Contract interpretation
- Breach of contract cases''',
                'excerpt': 'Learn the fundamental principles of contract formation, including offer, acceptance, and consideration.',
                'author': 'Attorney Lisa Martinez',
            },
        ]
        
        for article_data in articles:
            article, created = Article.objects.get_or_create(
                slug=article_data['slug'],
                defaults=article_data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'[OK] Article created: {article_data["title"]}'))
        
        # Create Exam Materials
        exam_materials = [
            {
                'category': categories_dict['Criminal Law'],
                'title': 'Criminal Law Exam Preparation Guide',
                'description': 'Comprehensive study guide covering all major topics in criminal law for exam preparation.',
                'order': 1,
            },
            {
                'category': categories_dict['Criminal Procedure'],
                'title': 'Criminal Procedure Practice Questions',
                'description': 'Practice questions and answers for criminal procedure examinations.',
                'order': 1,
            },
        ]
        
        for material_data in exam_materials:
            material, created = ExamMaterial.objects.get_or_create(
                title=material_data['title'],
                category=material_data['category'],
                defaults=material_data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'[OK] Exam material created: {material_data["title"]}'))
        
        # Create Game Types
        game_types = [
            {
                'name': 'Courtroom Simulation',
                'game_type': 'courtroom',
                'description': 'Experience realistic courtroom scenarios. Make decisions as a judge, investigator, or defense attorney.',
                'icon': '⚖️',
                'order': 1,
            },
            {
                'name': 'Criminal Case Analysis',
                'game_type': 'criminal_case',
                'description': 'Analyze evidence, formulate hypotheses, and select correct legal qualifications.',
                'icon': '🕵️',
                'order': 2,
            },
            {
                'name': 'Legal Tests & Quizzes',
                'game_type': 'quiz',
                'description': 'Test your knowledge of legal provisions and articles with interactive quizzes.',
                'icon': '📚',
                'order': 3,
            },
            {
                'name': 'Correct or Incorrect Scenarios',
                'game_type': 'scenario',
                'description': 'Evaluate real legal situations and determine if actions are correct or incorrect.',
                'icon': '🧠',
                'order': 4,
            },
        ]
        
        game_types_dict = {}
        for gt_data in game_types:
            game_type, created = GameType.objects.get_or_create(
                name=gt_data['name'],
                defaults=gt_data
            )
            game_types_dict[gt_data['name']] = game_type
            if created:
                self.stdout.write(self.style.SUCCESS(f'[OK] Game type created: {gt_data["name"]}'))
        
        # Create Games
        courtroom_game, created = Game.objects.get_or_create(
            title='Theft Case: Judge Decision',
            game_type=game_types_dict['Courtroom Simulation'],
            defaults={
                'description': 'You are the judge in a theft case. Review the evidence and make your decision.',
                'scenario': '''You are presiding over a theft case. The defendant is accused of stealing a laptop from a university library. 

The prosecution presents:
- Security camera footage showing the defendant taking the laptop
- Testimony from a library staff member who saw the incident
- The laptop was found in the defendant's possession

The defense argues:
- The defendant had permission to borrow the laptop
- There was no intent to permanently deprive the owner
- The security footage is unclear

You must evaluate the evidence and make a decision based on the law.''',
                'points_per_question': 20,
            }
        )
        
        if created:
            # Create questions for this game
            q1, _ = GameQuestion.objects.get_or_create(
                game=courtroom_game,
                question_text='Based on the evidence presented, what is the most appropriate legal standard to apply?',
                defaults={
                    'question_type': 'multiple_choice',
                    'order': 1,
                    'points': 20,
                }
            )
            
            GameAnswer.objects.get_or_create(
                question=q1,
                answer_text='Beyond a reasonable doubt - the highest standard for criminal cases',
                defaults={'is_correct': True, 'explanation': 'Correct! Criminal cases require proof beyond a reasonable doubt.', 'order': 1}
            )
            GameAnswer.objects.get_or_create(
                question=q1,
                answer_text='Preponderance of evidence - more likely than not',
                defaults={'is_correct': False, 'explanation': 'This is the standard for civil cases, not criminal.', 'order': 2}
            )
            GameAnswer.objects.get_or_create(
                question=q1,
                answer_text='Clear and convincing evidence',
                defaults={'is_correct': False, 'explanation': 'This standard is used in some civil cases, not criminal theft.', 'order': 3}
            )
            
            q2, _ = GameQuestion.objects.get_or_create(
                game=courtroom_game,
                question_text='What element of theft is most critical in this case?',
                defaults={
                    'question_type': 'multiple_choice',
                    'order': 2,
                    'points': 20,
                }
            )
            
            GameAnswer.objects.get_or_create(
                question=q2,
                answer_text='Intent to permanently deprive the owner',
                defaults={'is_correct': True, 'explanation': 'Correct! The intent to permanently deprive is a key element of theft.', 'order': 1}
            )
            GameAnswer.objects.get_or_create(
                question=q2,
                answer_text='Value of the stolen property',
                defaults={'is_correct': False, 'explanation': 'While value matters for sentencing, intent is the critical element.', 'order': 2}
            )
            GameAnswer.objects.get_or_create(
                question=q2,
                answer_text='Location where the theft occurred',
                defaults={'is_correct': False, 'explanation': 'Location is not a required element for theft.', 'order': 3}
            )
            
            self.stdout.write(self.style.SUCCESS('[OK] Courtroom Simulation game created with questions'))
        
        # Create Criminal Case Analysis Game
        case_game, created = Game.objects.get_or_create(
            title='Burglary Investigation',
            game_type=game_types_dict['Criminal Case Analysis'],
            defaults={
                'description': 'Analyze evidence and determine the correct legal qualification for a burglary case.',
                'scenario': '''You are investigating a burglary case. A residential home was broken into during the night. 

Evidence collected:
- Broken window on the ground floor
- Fingerprints on the window frame
- Missing jewelry and electronics
- Footprints in the garden
- Neighbor saw a suspicious vehicle at 2 AM

You must analyze the evidence and determine the appropriate legal qualification.''',
                'points_per_question': 25,
            }
        )
        
        if created:
            q1, _ = GameQuestion.objects.get_or_create(
                game=case_game,
                question_text='What is the most appropriate legal qualification for this case?',
                defaults={
                    'question_type': 'multiple_choice',
                    'order': 1,
                    'points': 25,
                }
            )
            
            GameAnswer.objects.get_or_create(
                question=q1,
                answer_text='Burglary - entering a building with intent to commit a crime',
                defaults={'is_correct': True, 'explanation': 'Correct! This meets the elements of burglary.', 'order': 1}
            )
            GameAnswer.objects.get_or_create(
                question=q1,
                answer_text='Theft - taking property without permission',
                defaults={'is_correct': False, 'explanation': 'While theft occurred, the entry into the building makes this burglary.', 'order': 2}
            )
            GameAnswer.objects.get_or_create(
                question=q1,
                answer_text='Trespassing - unauthorized entry',
                defaults={'is_correct': False, 'explanation': 'Trespassing is a lesser charge; the intent to commit a crime elevates this to burglary.', 'order': 3}
            )
            
            self.stdout.write(self.style.SUCCESS('[OK] Criminal Case Analysis game created'))
        
        # Create Legal Cases
        legal_cases = [
            {
                'title': 'Assault Case: Bar Fight',
                'case_type': 'criminal',
                'description': 'A case involving an altercation at a bar that resulted in injuries.',
                'scenario': '''On the evening of March 15, 2024, an altercation occurred at "The Legal Eagle" bar. 

Facts:
- Two individuals, John Doe and Jane Smith, were involved in a verbal argument
- The argument escalated when John threw a glass at Jane
- Jane sustained a cut on her face requiring 5 stitches
- Security footage shows the incident from multiple angles
- Several witnesses were present

You must analyze this case and determine the appropriate legal qualification and potential defenses.''',
                'evidence': '''Evidence Available:
1. Security camera footage (multiple angles)
2. Medical report from emergency room
3. Witness statements (5 witnesses)
4. Police report
5. Photos of the scene
6. Jane\'s statement
7. John\'s statement (claims self-defense)''',
            },
            {
                'title': 'Contract Dispute: Service Agreement',
                'case_type': 'civil',
                'description': 'A civil case involving a breach of service contract.',
                'scenario': '''ABC Company entered into a service agreement with XYZ Services on January 1, 2024.

Key Facts:
- Contract was for 12 months of IT support services
- ABC Company paid $50,000 upfront
- XYZ Services failed to provide services after 3 months
- ABC Company terminated the contract and seeks damages
- XYZ Services claims ABC Company breached first by changing requirements

Analyze the contract terms, breach claims, and potential remedies.''',
                'evidence': '''Evidence Available:
1. Original service agreement contract
2. Payment records
3. Email correspondence
4. Service logs
5. Change request documents
6. Termination notice
7. Financial impact analysis''',
            },
        ]
        
        for case_data in legal_cases:
            case, created = LegalCase.objects.get_or_create(
                title=case_data['title'],
                defaults=case_data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'[OK] Legal case created: {case_data["title"]}'))
        
        # Create News Categories
        news_categories = [
            {'name': 'Legal News', 'slug': 'legal-news'},
            {'name': 'Legislative Updates', 'slug': 'legislative-updates'},
            {'name': 'Case Studies', 'slug': 'case-studies'},
            {'name': 'Professional Opinions', 'slug': 'professional-opinions'},
        ]
        
        news_cats_dict = {}
        for cat_data in news_categories:
            category, created = NewsCategory.objects.get_or_create(
                slug=cat_data['slug'],
                defaults=cat_data
            )
            news_cats_dict[cat_data['slug']] = category
            if created:
                self.stdout.write(self.style.SUCCESS(f'[OK] News category created: {cat_data["name"]}'))
        
        # Create News Articles
        news_articles = [
            {
                'category': news_cats_dict['legal-news'],
                'title': 'New Criminal Justice Reform Bill Passes',
                'slug': 'criminal-justice-reform-bill-passes',
                'content': '''A significant criminal justice reform bill has been passed by the legislature, introducing changes to sentencing guidelines and rehabilitation programs.

The bill includes:
- Revised sentencing guidelines for non-violent offenses
- Enhanced rehabilitation programs
- Improved access to legal representation
- Changes to bail procedures

Legal professionals are encouraged to review the new provisions and their implications for ongoing and future cases.''',
                'excerpt': 'Major criminal justice reform legislation introduces new sentencing guidelines and rehabilitation programs.',
                'author': 'Legal News Team',
                'is_featured': True,
            },
            {
                'category': news_cats_dict['legislative-updates'],
                'title': 'Updates to Civil Procedure Rules',
                'slug': 'updates-civil-procedure-rules',
                'content': '''The Supreme Court has announced updates to civil procedure rules that will take effect next month.

Key changes include:
- Electronic filing requirements
- Updated discovery procedures
- Modified timeline for responses
- New mediation requirements

All legal practitioners should familiarize themselves with these changes to ensure compliance.''',
                'excerpt': 'Important updates to civil procedure rules affect filing, discovery, and case timelines.',
                'author': 'Editorial Staff',
            },
            {
                'category': news_cats_dict['case-studies'],
                'title': 'Landmark Contract Law Case Analysis',
                'slug': 'landmark-contract-law-case-analysis',
                'content': '''A recent Supreme Court decision has clarified important aspects of contract interpretation and enforcement.

The case involved:
- Interpretation of ambiguous contract terms
- Good faith and fair dealing requirements
- Remedies for breach of contract
- Statute of limitations considerations

This decision provides important guidance for contract drafting and dispute resolution.''',
                'excerpt': 'Recent Supreme Court decision provides clarity on contract interpretation and enforcement.',
                'author': 'Dr. Sarah Johnson',
                'is_featured': True,
            },
        ]
        
        for article_data in news_articles:
            article, created = NewsArticle.objects.get_or_create(
                slug=article_data['slug'],
                defaults=article_data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'[OK] News article created: {article_data["title"]}'))
        
        self.stdout.write(self.style.SUCCESS('\n[SUCCESS] All content populated successfully!'))
        self.stdout.write(self.style.SUCCESS('You can now access the website and see all the content.'))

