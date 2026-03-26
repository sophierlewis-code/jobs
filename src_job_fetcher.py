"""Fetch job data from sources or use sample data"""
from typing import List
from src.models import Job

class JobFetcher:
    """Fetch jobs from various sources"""
    
    @staticmethod
    def get_sample_jobs() -> List[Job]:
        """Get sample jobs for testing"""
        return [
            Job(
                id="1",
                title="Forest Governance Specialist - Remote",
                organization="Global Forest Alliance",
                description="""Join our team as a Forest Governance Specialist working on tenure security and land rights
                in Southeast Asia. You will facilitate workshops, conduct policy research, and support
                international consultancy rosters. Expertise in forest governance, land rights,
                and Indigenous Peoples rights required. Remote position, work from anywhere.""",
                location="Remote",
                job_type="remote",
                url="https://example.com/job/1",
                salary_range="$50,000 - $70,000"
            ),
            Job(
                id="2",
                title="Environmental Policy Officer - UK",
                organization="International Governance Institute",
                description="""Policy advisory role based in UK office or remote. Support MEL and donor reporting
                for climate and environmental projects. Strong research skills, facilitation experience,
                and understanding of sustainability policy required.""",
                location="United Kingdom",
                job_type="hybrid",
                url="https://example.com/job/2",
                salary_range="£35,000 - £45,000"
            ),
            Job(
                id="3",
                title="Land Rights Consultant - Bangkok, Thailand",
                organization="Regional Conservation NGO",
                description="""REJECTED: Thai nationals only. Must have Thai work permit.
                Fluent Thai required. Onsite position in Bangkok office.""",
                location="Bangkok, Thailand",
                job_type="onsite",
                url="https://example.com/job/3"
            ),
            Job(
                id="4",
                title="Grants Manager - International Consultancy",
                organization="Donor Coordination Network",
                description="""International consultant roster position. Support grant management and donor
                reporting for environmental and conservation programs. Work with teams across
                Southeast Asia and beyond. Remote, flexible schedule.
                Experience with MEL frameworks and monitoring/evaluation essential.""",
                location="International",
                job_type="remote",
                url="https://example.com/job/4",
                salary_range="$60,000 - $80,000"
            ),
            Job(
                id="5",
                title="Research Officer - Climate and Forests",
                organization="Academic Research Center",
                description="""Research position studying forest governance and climate adaptation in tropical
                regions, particularly Southeast Asia. Policy analysis, literature review, and
                stakeholder engagement. Work from anywhere option available.""",
                location="Global",
                job_type="remote",
                url="https://example.com/job/5",
                salary_range="$45,000 - $65,000"
            ),
            Job(
                id="6",
                title="Workshop Facilitator - Tenure and Rights",
                organization="International Rights Organization",
                description="""Design and facilitate training workshops on land tenure, Indigenous Peoples rights,
                and resource governance. Travel to Southeast Asia and other regions. Remote base,
                international role. Strong facilitation and training experience required.""",
                location="International",
                job_type="remote",
                url="https://example.com/job/6",
                salary_range="$55,000 - $75,000"
            ),
            Job(
                id="7",
                title="Java Developer - London",
                organization="Tech Startup",
                description="""Senior Java developer role. Build enterprise applications. Required: 5+ years Java,
                Spring Framework, microservices. No environmental or policy background needed.""",
                location="London, UK",
                job_type="onsite",
                url="https://example.com/job/7",
                salary_range="£60,000 - £80,000"
            ),
            Job(
                id="8",
                title="Programme Officer - Sustainable Development",
                organization="UN Agency",
                description="""Support programmes on sustainable development, environmental policy, and
                community engagement. International roster position. English speaking required.
                Preference for candidates with Southeast Asia expertise.""",
                location="Remote",
                job_type="remote",
                url="https://example.com/job/8",
                salary_range="UN salary scale"
            ),
        ]