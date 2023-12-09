import {LabelSmall, LabelLarge} from 'baseui/typography';
import Upload from 'baseui/icon/upload';
import {Button, KIND, SIZE} from 'baseui/button';
import {styled} from 'baseui';
import type {RestoRec} from '../pages';

const Container = styled('div', ({$theme}) => ({
  padding: '8px 16px',
  borderBottom: `1px solid ${$theme.colors.borderOpaque}`,
  display: 'flex',
  alignItems: 'center',
  justifyContent: 'space-between',
}));

const Group = styled('div', {
  display: 'flex',
  alignItems: 'center',
  justifyContent: 'space-between',
  gap: '8px',
});

const TitleGroup = styled('div', {
  display: 'flex',
  alignItems: 'center',
  justifyContent: 'space-between',
  gap: '12px',
});

export const Header = ({
  setRestoRecs,
  setAboutModalIsOpen,
}: {
  setRestoRecs: (recs: RestoRec[]) => void;
  setAboutModalIsOpen: (isOpen: boolean) => void;
}) => {
  return (
    <Container>
      <TitleGroup>
        <LabelSmall>
          CHOMPT
        </LabelSmall>
        <LabelLarge>
          |
        </LabelLarge>
        <LabelSmall>
          An AI restaurant choooser
        </LabelSmall>
      </TitleGroup>
      <Group>
        <Button
          size={SIZE.compact}
          kind={KIND.tertiary}
          onClick={() => setAboutModalIsOpen(true)}
        >
          About
        </Button>

        <Button
          startEnhancer={<Upload />}
          size={SIZE.compact}
          kind={KIND.secondary}
          onClick={() => setRestoRecs([])}
        >
          Reset
        </Button>
      </Group>
    </Container>
  );
};
