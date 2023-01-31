import SearchView from '../components/SearchView';
import VideoListWithFiltering from '../components/VideoListWithFiltering';
import Title from '../components/Title';
export default function SearchByTag() {
    return (
          <>
            <Title title="Search by Tag" />
            <VideoListWithFiltering />
          </>
    );
}
